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
    // const CSRANKING_PATH = './raw data - csranking/csrankings.csv'

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

        // look up names in google scholar
        const nameQuery = salName.replace(/\./g, '').replace(/ /g, '+')
        const gScholarQuery = 'https://scholar.google.com/citations?view_op=search_authors&mauthors=' + nameQuery
        const htmlStr = await axios.get(gScholarQuery).then((r) => r.data)
        const $ = cheerio.load(htmlStr)

        // get all h3 with class 'gs_ai_name'
        const gsAiNames = $('h3.gs_ai_name')
        if (gsAiNames.length === 0) {
            log(`${salName}: ${redLogStart}no google scholar entries found${redLogEnd}`)
            continue
        }

        // log('found:', gsAiNames.length)

        // click on first link
        // get citations
        // get h-index
        // get i10-index
    }
}
await main()
