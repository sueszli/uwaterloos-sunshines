import fs from 'fs'
import { assert, log } from 'console'

const main = async () => {
    const PATH_2021 = './data salaries/uw salaries 2021.csv'
    const PATH_2022 = './data salaries/uw salaries 2022.csv'
    const PATH_OUT = './merged salaries.csv'

    const str2021 = fs.readFileSync(PATH_2021, 'utf-8')
    const str2022 = fs.readFileSync(PATH_2022, 'utf-8')
    assert(str2021.split('\n')[0] === str2022.split('\n')[0])

    const header = str2021.split('\n')[0]
    fs.writeFileSync(PATH_OUT, header)

    const parsed2021 = str2021
        .split('\n')
        .slice(1)
        .map((line) => line.split(';'))
    const parsed2022 = str2022
        .split('\n')
        .slice(1)
        .map((line) => line.split(';'))

    // find entries in 2021 missing in 2022
    const missingEntries = []
    parsed2021.forEach((entry) => {
        const fst = entry[0]
        const snd = entry[1]
        const foundEntry = parsed2022.find((e) => e[0] === fst && e[1] === snd)
        if (!foundEntry) {
            log('data fallback because of missing entry:', fst, snd)
            missingEntries.push(entry)
        }
    })

    // mergedEntries = everything from 2022 + entries from 2021 that are missing in 2022
    const mergedEntries = parsed2022.concat(missingEntries)
    // join with semicolon
    mergedEntries.forEach((entry, i) => {
        mergedEntries[i] = entry.join(';')
    })
    fs.writeFileSync(PATH_OUT, mergedEntries.join('\n'))
}
await main()
