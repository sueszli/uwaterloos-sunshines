import fs from 'fs'
import { assert, log } from 'console'
import axios from 'axios'
import * as cheerio from 'cheerio'

const redLogStart = '\x1b[31m'
const redLogEnd = '\x1b[0m'
const greenLogStart = '\x1b[32m'
const greenLogEnd = '\x1b[0m'

const main = async () => {
    const SALARIES_PATH = './raw data - salaries/uw salaries merged.csv'
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

    let progress = 0
    let numSuccess = 0
    let numFailure = 0

    parsedSAL.forEach((salEntry) => {
        const salLastname = salEntry[0].toLowerCase()
        const salFirstname = salEntry[1].toLowerCase()

        const lastNameMatches = parsedCSR
            .filter((csrEntry) => {
                const csrNameElems = csrEntry[0].toLowerCase().split(' ')
                return csrNameElems.find((elem) => elem === salLastname)
            })
            .map((e) => e[0])
        if (lastNameMatches.length == 0) {
            numFailure++
        } else {
            numSuccess++
        }

        const progressPercent = Math.floor((progress++ / parsedSAL.length) * 100)
        console.clear()
        console.log('progress:', progressPercent + '%')
    })

    console.log(`successful lastname search: ${numSuccess}`) // 929 of 2051 <---- this is way too low
    console.log(`failed lastname search: ${numFailure}`) // 1122 of 2051
}
await main()
