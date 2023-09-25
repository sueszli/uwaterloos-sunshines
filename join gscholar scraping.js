import fs, { link } from 'fs'
import { assert, log } from 'console'
import axios from 'axios'
import * as cheerio from 'cheerio'

const redLogStart = '\x1b[31m'
const redLogEnd = '\x1b[0m'
const greenLogStart = '\x1b[32m'
const greenLogEnd = '\x1b[0m'

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

        // find google scholar entry
        const nameQuery = salName.replace(/\./g, '').replace(/ /g, '+')
        const gScholarQuery = 'https://scholar.google.com/citations?view_op=search_authors&mauthors=' + nameQuery
        const htmlStr = await axios.get(gScholarQuery).then((r) => r.data) // <--- this got me blocked
        const $ = cheerio.load(htmlStr)

        // find first links
        const links = $('a.gs_ai_pho')
        if (links.length === 0) {
            log(`${salName}: ${redLogStart}no google scholar entries found${redLogEnd}`)
            numFailure++
            continue
        }
        if (link.length > 1) {
            log(`${salName}: multiple google scholar entries found`)
        }

        // click on first link
        const link = links[0]
        const subHtmlStr = await axios.get(link).then((r) => r.data)
        const $sub = cheerio.load(subHtmlStr)
        const table = $sub('table#gsc_rsb_st')
        log(table)

        await new Promise((resolve) => setTimeout(resolve, 1000))
    }
}
await main()
