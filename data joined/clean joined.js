import fs, { link } from 'fs'
import { assert, log } from 'console'

const redLogStart = '\x1b[31m'
const redLogEnd = '\x1b[0m'
const greenLogStart = '\x1b[32m'
const greenLogEnd = '\x1b[0m'

const main = async () => {
    const INPUT_PATH = './data joined/joined.csv'
    const OUTPUT_PATH = './data joined/joined clean.csv'

    const strInput = fs.readFileSync(INPUT_PATH, 'utf-8').toLowerCase() // make everything lowercase
    const strInputLines = strInput.split('\n').filter((line) => !line.includes('unknown')) // remove lines with 'unknown'

    // write back
    fs.writeFileSync(OUTPUT_PATH, strInputLines.join('\n'))
}
await main()
