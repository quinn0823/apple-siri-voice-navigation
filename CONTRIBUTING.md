# Contributing to Apple Siri Voice Navigation

## File Structure

```
apple-siri-voice-navigation
├── * build                  // (Ignored) Files built by build scripts
│   └── * standard           // (Ignored) Standard mod
│       └── * apple-siri-voice-navigation.zip   // (Ignored) Refer to Usage section
├── docs
│   ├── github               // Documentation for GitHub
│   │   ├── images
│   │   ├── readme
│   │   └── release_notes
│   ├── mod                  // Documentation for Mod Manager in-game
│   │   ├── descriptions
│   │   └── images
│   └── workshop             // Documentation for Workshop
│       ├── change_notes
│       ├── descriptions
│       └── images
├── navigation
│   ├── build                // BANK and GUID files built by FMOD Studio, with SII files
│   ├── commands             // Navigation commands
│   │   ├── ...              // Commands in each language
│   │   └── template.json    // A template with no content
│   └── projects             // FMOD Studio projects
│       └── template.zip     // Sound project template
├── scripts                  // Scripts for building the mod
│   ├── build.py             // Script in Python
│   ├── * config.ini         // (Ignored) User config file
│   └── config_default.ini   // Default config file
└── LICENSE                  // The GNU General Public License v3.0 (GPL-3.0)
```

## Languages [25+ Languages Across 46+ Regions]

> [!TIP]
> Don't know the ISO 3166-1 (alpha-2) two-letter country codes? Visit [Microsoft](https://www.microsoft.com) and select your language: `https://www.microsoft.com/en-us/` > `english_us.json`.

- arabic
    - arabic_sa
    - arabic_ww
- chinese
    - chinese_cn
    - chinese_cnsn (Shaanxi)
    - chinese_cnln (Liaoning)
    - chinese_cnsc (Sichuan)
    - chinese_cnsh (Shanghai)
    - chinese_tw
    - chinese_hk
- czech
    - czech_cz
- danish
    - danish_dk
- dutch
    - dutch_be
    - dutch_nl
- english
    - english_au
    - english_gb
    - english_gbsc (Scotland)
    - english_ie
    - english_in
    - english_us
    - english_za
- french
    - french_be
    - french_ca
    - french_fr
- german
    - german_ge
- greek
    - greek_gr
- hebrew
    - hebrew_il
- hungarian
    - hungarian_hu
- italian
    - italian_it
- japanese
    - japanese_jp
- korean
    - korean_kr
- nb (Norwegian Bokmål)
    - nb_no
- polish
    - polish_pl
- portuguese
    - portuguese_br
    - portuguese_pt
- romanian
    - romanian_ro
- russian
    - russian_ru
- slovak
    - slovak_sk
- slovenian
    - slovenian_si
- spanish
    - spanish_ar
    - spanish_cl
    - spanish_co
    - spanish_es
    - spanish_mx
- swedish
    - swedish_se
- thai
    - thai_th
- turkish
    - turkish_tr

## Regular Expressions

### Update the Version Number

Search

```regexp
(?<=\(|\*{2}|\])\d+\.\d+(\.\d+)?(?=\)|\*{2}|\[)
```

Replace

```
${version_number}
```

### Remove Bold and Color Tags

Search

```regexp
(\*{2}|\[\w+\])((\S+) ?\S(中国)\S ?- (\S+)( ?\S+( ?\d)?\S)?)(\*{2}|\[/?\w+\])
```

Replace

```
$2
```

### Add Bold or Color Tags

- **GitHub**

    Search

    ```regexp
    - ((\S+) ?\S(中国)\S ?- (\S+)( ?\S+( ?\d)?\S)?)
    ```

    Replace

    ```
    - **$1**
    ```

- **Workshop (BBCode)**

    Search

    ```regexp
    \[\*\]((\S+) ?\S(中国)\S ?- (\S+)( ?\S+( ?\d)?\S)?)
    ```

    Replace

    ```
    [*][b]$1[/b]
    ```

- **Mod**

    Search

    ```regexp
    \* ((\S+) ?\S(中国)\S ?- (\S+)( ?\S+( ?\d)?\S)?)
    ```

    Replace
    - Green (Added)

        ```
        * [green]$1[normal]
        ```

    - Blue (Improved)

        ```
        * [blue]$1[normal]
        ```

---

Published Date (Contributing): October 17, 2026
