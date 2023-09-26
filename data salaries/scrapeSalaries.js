import fs from 'fs'
import axios from 'axios'
import * as cheerio from 'cheerio'
import { log } from 'console'

const main = async () => {
    const URL_2021 = 'https://uwaterloo.ca/about/accountability/salary-disclosure-2021'
    const URL_2022 = 'https://uwaterloo.ca/about/accountability/salary-disclosure-2022'
    const url = URL_2022

    const htmlStr = await axios.get(url).then((r) => r.data)
    const $ = cheerio.load(htmlStr)
    const table = $('table')
    const csv = []

    // get header
    const header = []
    table.find('thead tr th').each((_, el) => {
        header.push($(el).text())
    })
    csv.push(header.join(';'))

    // get content
    table.find('tbody tr').each((_, el) => {
        const row = []
        $(el)
            .find('td')
            .each((_, el) => row.push($(el).text()))
        const rowStr = row.join(';')
        csv.push(rowStr)
    })
    const csvStr = csv.join('\n')

    // save to file
    const fileName = './uw_salary.csv'
    fs.writeFileSync(fileName, csvStr)
    log(`Saved to ${fileName}`)

    process.exit(0)
}
await main()
