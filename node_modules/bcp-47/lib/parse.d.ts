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
export function parse(tag: string, options?: Options | null | undefined): Schema;
/**
 * Called when an error occurs.
 */
export type Warning = (reason: string, code: number, offset: number) => undefined;
/**
 * Configuration.
 */
export type Options = {
    /**
     * By default, when an error is encountered, an empty object is returned.
     * When in forgiving mode, all found values up to the point of the error
     * are included (`boolean`, default: `false`).
     *
     * So, for example, where by default `en-GB-abcdefghi` an empty object is
     * returned (as the language variant is too long), in `forgiving` mode the
     * `language` of `schema` is populated with `en` and the `region` is
     * populated with `GB`.
     */
    forgiving?: boolean | null | undefined;
    /**
     * Whether to normalize legacy tags when possible (`boolean`, default:
     * `true`).
     *
     * For example, `i-klingon` does not match the BCP 47 language algorithm but
     * is considered valid by BCP 47 nonetheless.
     * It is suggested to use `tlh` instead (the ISO 639-3 code for Klingon).
     * When `normalize` is `true`, passing `i-klingon` or other deprecated tags,
     * is handled as if their suggested valid tag was given instead.
     */
    normalize?: boolean | null | undefined;
    /**
     * When given, `warning` is called when an error is encountered (optional).
     */
    warning?: Warning | null | undefined;
};
/**
 * Extension.
 */
export type Extension = {
    /**
     *   List of extensions.
     *
     *   Each extension must be between two and eight (inclusive) characters.
     */
    extensions: Array<string>;
    /**
     *   One character `singleton`.
     *
     *   `singleton` cannot be `x` (case insensitive).
     */
    singleton: string;
};
/**
 * Parsed language tag.
 *
 * A schema is deemed empty when it has neither `language`, `irregular`,
 * `regular`, nor `privateuse` (where an empty `privateuse` array is handled
 * as no `privateuse` as well).
 */
export type Schema = {
    /**
     *   Selected three-character ISO 639 codes, such as
     *   `yue` in `zh-yue-HK` (Chinese, Cantonese, as used in Hong Kong SAR).
     */
    extendedLanguageSubtags: Array<string>;
    /**
     *   List of extensions, each an object containing a one character `singleton`,
     *   and a list of `extensions`.
     *
     *   `singleton` cannot be `x` (case insensitive) and `extensions` must be
     *   between two and eight (inclusive) characters.
     *
     *   For example, an extension would be `u-co-phonebk` in `de-DE-u-co-phonebk`
     *   (German, as used in Germany, using German phonebook sort order), where `u`
     *   is the `singleton` and `co` and `phonebk` are its extensions.
     */
    extensions: Array<Extension>;
    /**
     *   One of the `irregular` tags: tags that are seen as invalid by the
     *   algorithm).
     *
     *   Valid values are: `'en-GB-oed'`, `'i-ami'`, `'i-bnn'`, `'i-default'`,
     *   `'i-enochian'`, `'i-hak'`, `'i-klingon'`, `'i-lux'`, `'i-mingo'`,
     *   `'i-navajo'`, `'i-pwn'`, `'i-tao'`, `'i-tay'`, `'i-tsu'`, `'sgn-BE-FR'`,
     *   `'sgn-BE-NL'`, `'sgn-CH-DE'`.
     */
    irregular: string | null | undefined;
    /**
     *   Two or three character ISO 639 language code, four character reserved
     *   language code, or 5 to 8 (inclusive) characters registered language subtag.
     *
     *   For example, `en` (English) or `cmn` (Mandarin Chinese).
     */
    language: string | null | undefined;
    /**
     *   List of private-use subtags, where each subtag must be between one and
     *   eight (inclusive) characters.
     */
    privateuse: Array<string>;
    /**
     *   Two alphabetical character ISO 3166-1 code or three digit UN M49 code.
     *
     *   For example, `CN` in `cmn-Hans-CN` (Mandarin Chinese, Simplified script,
     *   as used in China) or `419` in `es-419` (Spanish as used in Latin America
     *   and the Caribbean).
     */
    region: string | null | undefined;
    /**
     *   One of the `regular` tags: tags that are seen as something different
     *   by the algorithm.
     *
     *   Valid values are: `'art-lojban'`, `'cel-gaulish'`, `'no-bok'`, `'no-nyn'`,
     *   `'zh-guoyu'`, `'zh-hakka'`, `'zh-min'`, `'zh-min-nan'`, and `'zh-xiang'`.
     */
    regular: string | null | undefined;
    /**
     *   Four character ISO 15924 script code, such as `Latn` in
     *   `hy-Latn-IT-arevela` (Eastern Armenian written in Latin script, as used in
     *   Italy).
     */
    script: string | null | undefined;
    /**
     *   5 to 8 (inclusive) character language variants, such as `rozaj` and
     *   `biske` in `sl-rozaj-biske` (San Giorgio dialect of Resian dialect of
     *   Slovenian).
     */
    variants: Array<string>;
};
//# sourceMappingURL=parse.d.ts.map