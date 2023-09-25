import fs from 'fs'
import { assert, log } from 'console'

const main = async () => {
    const PATH_2021 = './raw data - salaries/XYZ.csv'
    const PATH_2022 = './raw data - salaries/XYZ.csv'

    const str2021 = fs.readFileSync(PATH_2021, 'utf-8')
    const str2022 = fs.readFileSync(PATH_2022, 'utf-8')

    assert(str2021.split('\n')[0] === str2022.split('\n')[0])

    const parsed2021 = str2021
        .split('\n')
        .slice(1)
        .map((line) => line.split(','))
    const parsed2022 = str2022
        .split('\n')
        .slice(1)
        .map((line) => line.split(','))

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

    // save 2022 + missing entries as 'mergedEntries'
    const mergedEntries = parsed2022.concat(missingEntries)
    fs.writeFileSync('./joinedSalaries.csv', mergedEntries.join('\n'))
}
await main()
