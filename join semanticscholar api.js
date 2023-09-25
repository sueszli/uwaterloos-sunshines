import fs, { link } from 'fs'
import { assert, log } from 'console'
import axios from 'axios'
import * as cheerio from 'cheerio'

const redLogStart = '\x1b[31m'
const redLogEnd = '\x1b[0m'
const greenLogStart = '\x1b[32m'
const greenLogEnd = '\x1b[0m'

let progress = 0
let numSuccess = 0
let numFailure = 0

const main = async () => {
    const SALARIES_PATH = './raw data - salaries/uw salaries merged.csv'

    const strSAL = fs.readFileSync(SALARIES_PATH, 'utf-8')
    const parsedSAL = strSAL
        .split('\n')
        .slice(1)
        .map((line) => line.split(','))

    for (let i = 0; i < parsedSAL.length; i++) {
        const salEntry = parsedSAL[i]

        const salLastname = salEntry[0].toLowerCase()
        const salFirstname = salEntry[1].toLowerCase()
        const salName = [salFirstname, salLastname].join(' ').toLowerCase()

        const nameQuery = salName.replace(/\./g, '').replace(/ /g, '+')
        const fullQuery = 'https://api.semanticscholar.org/graph/v1/author/search?query=' + nameQuery
        const json = await axios.get(fullQuery).then((r) => r.data)

        const length = json.total
        if (json.total == 0) {
            numFailure++
        } else {
            numSuccess++
        }

        // log(nameQuery, json)

        // await new Promise((resolve) => setTimeout(resolve, 3000))

        const progressPercent = Math.floor((progress++ / parsedSAL.length) * 100)
        console.clear()
        console.log('progress:', progressPercent + '%')
    }
    console.log(`successful lastname search: ${numSuccess}`) // 929 of 2051 <---- this is way too low
    console.log(`failed lastname search: ${numFailure}`) // 1122 of 2051
}
await main()
