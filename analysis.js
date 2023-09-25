import fs from 'fs'
import { assert, log } from 'console'
import axios from 'axios'
import * as cheerio from 'cheerio'

const redLogStart = '\x1b[31m'
const redLogEnd = '\x1b[0m'
const greenLogStart = '\x1b[32m'
const greenLogEnd = '\x1b[0m'

const main = async () => {
    const SALARIES_PATH = './raw data - salary disclosure/uw salaries merged.csv'
    const CSRANKING_PATH = './raw data - csranking/csrankings.csv'

    const strSAL = fs.readFileSync(SALARIES_PATH, 'utf-8')
    const parsedSAL = strSAL
        .split('\n')
        .slice(1)
        .map((line) => line.split(','))

    const strCSR = fs.readFileSync(CSRANKING_PATH, 'utf-8')
    const parsedCSR = strCSR
        .split('\n')
        .slice(1)
        .map((line) => line.split(','))

    for (let i = 0; i < parsedSAL.length; i++) {
        const salEntry = parsedSAL[i]

        const salLastname = salEntry[0].toLowerCase()
        const salFirstname = salEntry[1].toLowerCase()
        const salName = [salFirstname, salLastname].join(' ').toLowerCase()

        for (let j = 0; j < parsedCSR.length; j++) {
            const csrEntry = parsedCSR[j]
            const csrName = csrEntry[0].toLowerCase()

            const matchedLastName = csrName.includes(salLastname)
            if (!matchedLastName) {
                // fuck
            } else {
                // check if first name matches aswell
            }
        }
    }
}
await main()
