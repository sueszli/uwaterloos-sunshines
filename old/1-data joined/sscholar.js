import fs, { link } from 'fs'
import { assert, log } from 'console'
import axios from 'axios'

const redLogStart = '\x1b[31m'
const redLogEnd = '\x1b[0m'
const greenLogStart = '\x1b[32m'
const greenLogEnd = '\x1b[0m'

const main = async () => {
    const SALARIES_PATH = './data salaries/merged salaries.csv'

    const strSAL = fs.readFileSync(SALARIES_PATH, 'utf-8')
    const parsedSAL = strSAL
        .split('\n')
        .slice(1)
        .map((line) => line.split(';'))

    const OUTPUT_PATH = './joinedTable.csv'
    const header = [
        'surname',
        'given name',
        'position title',
        'salary paid',
        'taxable benefits', // from salary disclosure

        'paperCount',
        'citationCount',
        'hIndex', // from semantic scholar
    ]
    fs.writeFileSync(OUTPUT_PATH, header.join(';') + '\n')

    let progress = 0

    for (let i = 0; i < parsedSAL.length; i++) {
        const salEntry = parsedSAL[i]
        const salLastname = salEntry[0].toLowerCase()
        const salFirstname = salEntry[1].toLowerCase()
        const salName = [salFirstname, salLastname].join(' ').toLowerCase()

        // query semantic scholar
        const nameQuery = salName.replace(/\./g, '').replace(/ /g, '+')
        const fullQuery = 'https://api.semanticscholar.org/graph/v1/author/search?query=' + nameQuery
        const json = await axios.get(fullQuery).then((r) => r.data)

        assert(json.hasOwnProperty('total'))
        if (json.total == 0) {
            log(`${salName}: ${redLogStart}no semantic scholar entries found${redLogEnd}`)
            const newEntry = [...salEntry, 'UNKNOWN', 'UNKNOWN', 'UNKNOWN']
            const newEntryStr = newEntry.join(';')
            fs.appendFileSync(OUTPUT_PATH, newEntryStr + '\n')
        } else {
            // get closest name match
            const matches = json.data
            const perfectMatches = matches.filter(({ _, name }) => {
                name = name.toLowerCase()
                return name === salName
            })
            const fuzzyMatches = matches.filter(({ _, name }) => {
                name = name.toLowerCase()
                return name.includes(salFirstname) && name.includes(salLastname)
            })
            let closestMatch = null
            if (perfectMatches.length > 0) {
                closestMatch = perfectMatches[0]
            } else if (fuzzyMatches.length > 0) {
                closestMatch = fuzzyMatches[0]
            } else {
                closestMatch = matches[0]
            }
            assert(closestMatch !== null)
            assert(closestMatch.hasOwnProperty('authorId'))
            const closestMatchUrl = 'https://api.semanticscholar.org/graph/v1/author/' + closestMatch.authorId + '?fields=name,paperCount,citationCount,hIndex'

            // query semantic scholar for closest match
            const { authorId, name, paperCount, citationCount, hIndex } = await axios.get(closestMatchUrl).then((r) => r.data)
            const newEntry = [...salEntry, paperCount, citationCount, hIndex]

            // save to file
            const newEntryStr = newEntry.join(';')
            fs.appendFileSync(OUTPUT_PATH, newEntryStr + '\n')
        }

        progress++
        log(`progress: ${progress}/${parsedSAL.length}`)
    }
}
await main()
