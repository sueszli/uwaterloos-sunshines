import fs from 'fs'
import { assert, log } from 'console'
import axios from 'axios'
import * as cheerio from 'cheerio'

const main = async () => {
    const SALARIES_PATH = './raw data - salary disclosure/uw salaries merged.csv'
    // const CSRANKING_PATH = './raw data - csranking/csrankings.csv'

    const strSAL = fs.readFileSync(SALARIES_PATH, 'utf-8')
    const parsedSAL = strSAL
        .split('\n')
        .slice(1)
        .map((line) => line.split(','))

    // const strCSR = fs.readFileSync(CSRANKING_PATH, 'utf-8')
    // const parsedCSR = strCSR
    //     .split('\n')
    //     .slice(1)
    //     .map((line) => line.split(','))

    parsedSAL.forEach((salEntry) => {
        const salLastname = salEntry[0].toLowerCase()
        const salFirstname = salEntry[1].toLowerCase()
        const salName = [salFirstname, salLastname].join(' ').toLowerCase()

        const nameQuery = salName.replace(/\./g, '').replace(/ /g, '+')
        const gScholarQuery = 'https://scholar.google.com/citations?view_op=search_authors&mauthors=' + nameQuery

        // fetch

        // click on first link

        // get citations
        // get h-index
        // get i10-index
    })
}
await main()
