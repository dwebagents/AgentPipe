/**
 * @callback Warning
 *   Called when an error occurs.
 * @param {string} reason
 *   Reason for failure in English.
 * @param {number} code
 *   Code for failure.
 * @param {number} offset
 *   index of place where the error occurred in the tag
 * @returns {undefined}
 */

/**
 * @typedef Options
 *   Configuration.
 * @property {boolean | null | undefined} [forgiving=false]
 *   By default, when an error is encountered, an empty object is returned.
 *   When in forgiving mode, all found values up to the point of the error
 *   are included (`boolean`, default: `false`).
 *
 *   So, for example, where by default `en-GB-abcdefghi` an empty object is
 *   returned (as the language variant is too long), in `forgiving` mode the
 *   `language` of `schema` is populated with `en` and the `region` is
 *   populated with `GB`.
 * @property {boolean | null | undefined} [normalize=true]
 *   Whether to normalize legacy tags when possible (`boolean`, default:
 *   `true`).
 *
 *   For example, `i-klingon` does not match the BCP 47 language algorithm but
 *   is considered valid by BCP 47 nonetheless.
 *   It is suggested to use `tlh` instead (the ISO 639-3 code for Klingon).
 *   When `normalize` is `true`, passing `i-klingon` or other deprecated tags,
 *   is handled as if their suggested valid tag was given instead.
 * @property {Warning | null | undefined} [warning]
 *   When given, `warning` is called when an error is encountered (optional).
 */

/**
 * @typedef Extension
 *   Extension.
 * @property {Array<string>} extensions
 *   List of extensions.
 *
 *   Each extension must be between two and eight (inclusive) characters.
 * @property {string} singleton
 *   One character `singleton`.
 *
 *   `singleton` cannot be `x` (case insensitive).
 */

/**
 * @typedef Schema
 *   Parsed language tag.
 *
 *   A schema is deemed empty when it has neither `language`, `irregular`,
 *   `regular`, nor `privateuse` (where an empty `privateuse` array is handled
 *   as no `privateuse` as well).
 * @property {Array<string>} extendedLanguageSubtags
 *   Selected three-character ISO 639 codes, such as
 *   `yue` in `zh-yue-HK` (Chinese, Cantonese, as used in Hong Kong SAR).
 * @property {Array<Extension>} extensions
 *   List of extensions, each an object containing a one character `singleton`,
 *   and a list of `extensions`.
 *
 *   `singleton` cannot be `x` (case insensitive) and `extensions` must be
 *   between two and eight (inclusive) characters.
 *
 *   For example, an extension would be `u-co-phonebk` in `de-DE-u-co-phonebk`
 *   (German, as used in Germany, using German phonebook sort order), where `u`
 *   is the `singleton` and `co` and `phonebk` are its extensions.
 * @property {string | null | undefined} irregular
 *   One of the `irregular` tags: tags that are seen as invalid by the
 *   algorithm).
 *
 *   Valid values are: `'en-GB-oed'`, `'i-ami'`, `'i-bnn'`, `'i-default'`,
 *   `'i-enochian'`, `'i-hak'`, `'i-klingon'`, `'i-lux'`, `'i-mingo'`,
 *   `'i-navajo'`, `'i-pwn'`, `'i-tao'`, `'i-tay'`, `'i-tsu'`, `'sgn-BE-FR'`,
 *   `'sgn-BE-NL'`, `'sgn-CH-DE'`.
 * @property {string | null | undefined} language
 *   Two or three character ISO 639 language code, four character reserved
 *   language code, or 5 to 8 (inclusive) characters registered language subtag.
 *
 *   For example, `en` (English) or `cmn` (Mandarin Chinese).
 * @property {Array<string>} privateuse
 *   List of private-use subtags, where each subtag must be between one and
 *   eight (inclusive) characters.
 * @property {string | null | undefined} region
 *   Two alphabetical character ISO 3166-1 code or three digit UN M49 code.
 *
 *   For example, `CN` in `cmn-Hans-CN` (Mandarin Chinese, Simplified script,
 *   as used in China) or `419` in `es-419` (Spanish as used in Latin America
 *   and the Caribbean).
 * @property {string | null | undefined} regular
 *   One of the `regular` tags: tags that are seen as something different
 *   by the algorithm.
 *
 *   Valid values are: `'art-lojban'`, `'cel-gaulish'`, `'no-bok'`, `'no-nyn'`,
 *   `'zh-guoyu'`, `'zh-hakka'`, `'zh-min'`, `'zh-min-nan'`, and `'zh-xiang'`.
 * @property {string | null | undefined} script
 *   Four character ISO 15924 script code, such as `Latn` in
 *   `hy-Latn-IT-arevela` (Eastern Armenian written in Latin script, as used in
 *   Italy).
 * @property {Array<string>} variants
 *   5 to 8 (inclusive) character language variants, such as `rozaj` and
 *   `biske` in `sl-rozaj-biske` (San Giorgio dialect of Resian dialect of
 *   Slovenian).
 */

import {isAlphanumerical} from 'is-alphanumerical'
import {isAlphabetical} from 'is-alphabetical'
import {isDecimal} from 'is-decimal'
import {regular} from './regular.js'
import {normal} from './normal.js'

const own = {}.hasOwnProperty

/**
 * Parse a BCP 47 language tag.
 *
 * > 👉 **Note**: the algorithm is case insensitive.
 *
 * @param {string} tag
 *   BCP 47 tag to parse.
 * @param {Options | null | undefined} [options]
 *   Configuration (optional).
 * @returns {Schema}
 *   Parsed BCP 47 language tag.
 */
export function parse(tag, options) {
  const settings = options || {}
  const result = empty()
  const source = String(tag)
  const value = source.toLowerCase()
  let index = 0

  // Check input.
  if (tag === null || tag === undefined) {
    throw new Error('Expected string, got `' + tag + '`')
  }

  // Let’s start.
  // First: the edge cases.
  if (own.call(normal, value)) {
    const replacement = normal[value]

    if (
      (settings.normalize === null ||
        settings.normalize === undefined ||
        settings.normalize) &&
      typeof replacement === 'string'
    ) {
      return parse(replacement)
    }

    result[regular.includes(value) ? 'regular' : 'irregular'] = source

    return result
  }

  // Now, to actually parse, eat what could be a language.
  while (isAlphabetical(value.charCodeAt(index)) && index < 9) index++

  // A language.
  if (index > 1 /* Min 639. */ && index < 9 /* Max subtag. */) {
    // 5 and up is a subtag.
    // 4 is the size of reserved languages.
    // 3 an ISO 639-2 or ISO 639-3.
    // 2 is an ISO 639-1.
    // <https://github.com/wooorm/iso-639-2>
    // <https://github.com/wooorm/iso-639-3>
    result.language = source.slice(0, index)

    if (index < 4 /* Max 639. */) {
      let groups = 0

      while (
        value.charCodeAt(index) === 45 /* `-` */ &&
        isAlphabetical(value.charCodeAt(index + 1)) &&
        isAlphabetical(value.charCodeAt(index + 2)) &&
        isAlphabetical(value.charCodeAt(index + 3)) &&
        !isAlphanumerical(value.charCodeAt(index + 4))
      ) {
        if (groups > 2 /* Max extended language subtag count. */) {
          return fail(
            index,
            3,
            'Too many extended language subtags, expected at most 3 subtags'
          )
        }

        // Extended language subtag.
        result.extendedLanguageSubtags.push(source.slice(index + 1, index + 4))
        index += 4
        groups++
      }
    }

    // ISO 15924 script.
    // <https://github.com/wooorm/iso-15924>
    if (
      value.charCodeAt(index) === 45 /* `-` */ &&
      isAlphabetical(value.charCodeAt(index + 1)) &&
      isAlphabetical(value.charCodeAt(index + 2)) &&
      isAlphabetical(value.charCodeAt(index + 3)) &&
      isAlphabetical(value.charCodeAt(index + 4)) &&
      !isAlphanumerical(value.charCodeAt(index + 5))
    ) {
      result.script = source.slice(index + 1, index + 5)
      index += 5
    }

    if (value.charCodeAt(index) === 45 /* `-` */) {
      // ISO 3166-1 region.
      // <https://github.com/wooorm/iso-3166>
      if (
        isAlphabetical(value.charCodeAt(index + 1)) &&
        isAlphabetical(value.charCodeAt(index + 2)) &&
        !isAlphanumerical(value.charCodeAt(index + 3))
      ) {
        result.region = source.slice(index + 1, index + 3)
        index += 3
      }
      // UN M49 region.
      // <https://github.com/wooorm/un-m49>
      else if (
        isDecimal(value.charCodeAt(index + 1)) &&
        isDecimal(value.charCodeAt(index + 2)) &&
        isDecimal(value.charCodeAt(index + 3)) &&
        !isAlphanumerical(value.charCodeAt(index + 4))
      ) {
        result.region = source.slice(index + 1, index + 4)
        index += 4
      }
    }

    while (value.charCodeAt(index) === 45 /* `-` */) {
      const start = index + 1
      let offset = start

      while (isAlphanumerical(value.charCodeAt(offset))) {
        if (offset - start > 7 /* Max variant. */) {
          return fail(
            offset,
            1,
            'Too long variant, expected at most 8 characters'
          )
        }

        offset++
      }

      if (
        // Long variant.
        offset - start > 4 /* Min alpha numeric variant. */ ||
        // Short variant.
        (offset - start > 3 /* Min variant. */ &&
          isDecimal(value.charCodeAt(start)))
      ) {
        result.variants.push(source.slice(start, offset))
        index = offset
      }
      // Something else.
      else {
        break
      }
    }

    // Extensions.
    while (value.charCodeAt(index) === 45 /* `-` */) {
      // Exit if this isn’t an extension.
      if (
        value.charCodeAt(index + 1) === 120 /* `x` */ ||
        !isAlphanumerical(value.charCodeAt(index + 1)) ||
        value.charCodeAt(index + 2) !== 45 /* `-` */ ||
        !isAlphanumerical(value.charCodeAt(index + 3))
      ) {
        break
      }

      let offset = index + 2
      let groups = 0

      while (
        value.charCodeAt(offset) === 45 /* `-` */ &&
        isAlphanumerical(value.charCodeAt(offset + 1)) &&
        isAlphanumerical(value.charCodeAt(offset + 2))
      ) {
        const start = offset + 1
        offset = start + 2
        groups++

        while (isAlphanumerical(value.charCodeAt(offset))) {
          if (offset - start > 7 /* Max extension. */) {
            return fail(
              offset,
              2,
              'Too long extension, expected at most 8 characters'
            )
          }

          offset++
        }
      }

      if (!groups) {
        return fail(
          offset,
          4,
          'Empty extension, extensions must have at least 2 characters of content'
        )
      }

      result.extensions.push({
        extensions: source.slice(index + 3, offset).split('-'),
        singleton: source.charAt(index + 1)
      })

      index = offset
    }
  }
  // Not a language.
  else {
    index = 0
  }

  // Private use.
  if (
    (index === 0 && value.charCodeAt(index) === 120) /* `x` */ ||
    (value.charCodeAt(index) === 45 /* `-` */ &&
      value.charCodeAt(index + 1) === 120) /* `x` */
  ) {
    index = index ? index + 2 : 1
    let offset = index

    while (
      value.charCodeAt(offset) === 45 /* `-` */ &&
      isAlphanumerical(value.charCodeAt(offset + 1))
    ) {
      const start = index + 1
      offset = start

      while (isAlphanumerical(value.charCodeAt(offset))) {
        if (offset - start > 7 /* Max private use. */) {
          return fail(
            offset,
            5,
            'Too long private-use area, expected at most 8 characters'
          )
        }

        offset++
      }

      result.privateuse.push(source.slice(index + 1, offset))
      index = offset
    }
  }

  if (index !== source.length) {
    return fail(index, 6, 'Found superfluous content after tag')
  }

  return result

  /**
   * Stop.
   *
   * @param {number} offset
   * @param {number} code
   * @param {string} reason
   * @returns {Schema}
   */
  function fail(offset, code, reason) {
    if (settings.warning) settings.warning(reason, code, offset)
    return settings.forgiving ? result : empty()
  }
}

/**
 * Create an empty results object.
 *
 * @returns {Schema}
 */
function empty() {
  return {
    extendedLanguageSubtags: [],
    extensions: [],
    irregular: null,
    language: null,
    privateuse: [],
    region: null,
    regular: null,
    script: null,
    variants: []
  }
}
