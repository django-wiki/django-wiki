/*
Patched version of Django's URLify since Django put everything into a protected
namespace and hence we couldn't change its behavior from outside.
*/
/*global XRegExp*/
(function() {
    'use strict';

    var LATIN_MAP = {
        'Ã€': 'A', 'Ã': 'A', 'Ã‚': 'A', 'Ãƒ': 'A', 'Ã„': 'A', 'Ã…': 'A', 'Ã†': 'AE',
        'Ã‡': 'C', 'Ãˆ': 'E', 'Ã‰': 'E', 'ÃŠ': 'E', 'Ã‹': 'E', 'ÃŒ': 'I', 'Ã': 'I',
        'ÃŽ': 'I', 'Ã': 'I', 'Ã': 'D', 'Ã‘': 'N', 'Ã’': 'O', 'Ã“': 'O', 'Ã”': 'O',
        'Ã•': 'O', 'Ã–': 'O', 'Å': 'O', 'Ã˜': 'O', 'Ã™': 'U', 'Ãš': 'U', 'Ã›': 'U',
        'Ãœ': 'U', 'Å°': 'U', 'Ã': 'Y', 'Ãž': 'TH', 'Å¸': 'Y', 'ÃŸ': 'ss', 'Ã ': 'a',
        'Ã¡': 'a', 'Ã¢': 'a', 'Ã£': 'a', 'Ã¤': 'a', 'Ã¥': 'a', 'Ã¦': 'ae', 'Ã§': 'c',
        'Ã¨': 'e', 'Ã©': 'e', 'Ãª': 'e', 'Ã«': 'e', 'Ã¬': 'i', 'Ã­': 'i', 'Ã®': 'i',
        'Ã¯': 'i', 'Ã°': 'd', 'Ã±': 'n', 'Ã²': 'o', 'Ã³': 'o', 'Ã´': 'o', 'Ãµ': 'o',
        'Ã¶': 'o', 'Å‘': 'o', 'Ã¸': 'o', 'Ã¹': 'u', 'Ãº': 'u', 'Ã»': 'u', 'Ã¼': 'u',
        'Å±': 'u', 'Ã½': 'y', 'Ã¾': 'th', 'Ã¿': 'y'
    };
    var LATIN_SYMBOLS_MAP = {
        'Â©': '(c)'
    };
    var GREEK_MAP = {
        'Î±': 'a', 'Î²': 'b', 'Î³': 'g', 'Î´': 'd', 'Îµ': 'e', 'Î¶': 'z', 'Î·': 'h',
        'Î¸': '8', 'Î¹': 'i', 'Îº': 'k', 'Î»': 'l', 'Î¼': 'm', 'Î½': 'n', 'Î¾': '3',
        'Î¿': 'o', 'Ï€': 'p', 'Ï': 'r', 'Ïƒ': 's', 'Ï„': 't', 'Ï…': 'y', 'Ï†': 'f',
        'Ï‡': 'x', 'Ïˆ': 'ps', 'Ï‰': 'w', 'Î¬': 'a', 'Î­': 'e', 'Î¯': 'i', 'ÏŒ': 'o',
        'Ï': 'y', 'Î®': 'h', 'ÏŽ': 'w', 'Ï‚': 's', 'ÏŠ': 'i', 'Î°': 'y', 'Ï‹': 'y',
        'Î': 'i', 'Î‘': 'A', 'Î’': 'B', 'Î“': 'G', 'Î”': 'D', 'Î•': 'E', 'Î–': 'Z',
        'Î—': 'H', 'Î˜': '8', 'Î™': 'I', 'Îš': 'K', 'Î›': 'L', 'Îœ': 'M', 'Î': 'N',
        'Îž': '3', 'ÎŸ': 'O', 'Î ': 'P', 'Î¡': 'R', 'Î£': 'S', 'Î¤': 'T', 'Î¥': 'Y',
        'Î¦': 'F', 'Î§': 'X', 'Î¨': 'PS', 'Î©': 'W', 'Î†': 'A', 'Îˆ': 'E', 'ÎŠ': 'I',
        'ÎŒ': 'O', 'ÎŽ': 'Y', 'Î‰': 'H', 'Î': 'W', 'Îª': 'I', 'Î«': 'Y'
    };
    var TURKISH_MAP = {
        'ÅŸ': 's', 'Åž': 'S', 'Ä±': 'i', 'Ä°': 'I', 'Ã§': 'c', 'Ã‡': 'C', 'Ã¼': 'u',
        'Ãœ': 'U', 'Ã¶': 'o', 'Ã–': 'O', 'ÄŸ': 'g', 'Äž': 'G'
    };
    var ROMANIAN_MAP = {
        'Äƒ': 'a', 'Ã®': 'i', 'È™': 's', 'È›': 't', 'Ã¢': 'a',
        'Ä‚': 'A', 'ÃŽ': 'I', 'È˜': 'S', 'Èš': 'T', 'Ã‚': 'A'
    };
    var RUSSIAN_MAP = {
        'Ð°': 'a', 'Ð±': 'b', 'Ð²': 'v', 'Ð³': 'g', 'Ð´': 'd', 'Ðµ': 'e', 'Ñ‘': 'yo',
        'Ð¶': 'zh', 'Ð·': 'z', 'Ð¸': 'i', 'Ð¹': 'j', 'Ðº': 'k', 'Ð»': 'l', 'Ð¼': 'm',
        'Ð½': 'n', 'Ð¾': 'o', 'Ð¿': 'p', 'Ñ€': 'r', 'Ñ': 's', 'Ñ‚': 't', 'Ñƒ': 'u',
        'Ñ„': 'f', 'Ñ…': 'h', 'Ñ†': 'c', 'Ñ‡': 'ch', 'Ñˆ': 'sh', 'Ñ‰': 'sh', 'ÑŠ': '',
        'Ñ‹': 'y', 'ÑŒ': '', 'Ñ': 'e', 'ÑŽ': 'yu', 'Ñ': 'ya',
        'Ð': 'A', 'Ð‘': 'B', 'Ð’': 'V', 'Ð“': 'G', 'Ð”': 'D', 'Ð•': 'E', 'Ð': 'Yo',
        'Ð–': 'Zh', 'Ð—': 'Z', 'Ð˜': 'I', 'Ð™': 'J', 'Ðš': 'K', 'Ð›': 'L', 'Ðœ': 'M',
        'Ð': 'N', 'Ðž': 'O', 'ÐŸ': 'P', 'Ð ': 'R', 'Ð¡': 'S', 'Ð¢': 'T', 'Ð£': 'U',
        'Ð¤': 'F', 'Ð¥': 'H', 'Ð¦': 'C', 'Ð§': 'Ch', 'Ð¨': 'Sh', 'Ð©': 'Sh', 'Ðª': '',
        'Ð«': 'Y', 'Ð¬': '', 'Ð­': 'E', 'Ð®': 'Yu', 'Ð¯': 'Ya'
    };
    var UKRAINIAN_MAP = {
        'Ð„': 'Ye', 'Ð†': 'I', 'Ð‡': 'Yi', 'Ò': 'G', 'Ñ”': 'ye', 'Ñ–': 'i',
        'Ñ—': 'yi', 'Ò‘': 'g'
    };
    var CZECH_MAP = {
        'Ä': 'c', 'Ä': 'd', 'Ä›': 'e', 'Åˆ': 'n', 'Å™': 'r', 'Å¡': 's', 'Å¥': 't',
        'Å¯': 'u', 'Å¾': 'z', 'ÄŒ': 'C', 'ÄŽ': 'D', 'Äš': 'E', 'Å‡': 'N', 'Å˜': 'R',
        'Å ': 'S', 'Å¤': 'T', 'Å®': 'U', 'Å½': 'Z'
    };
    var POLISH_MAP = {
        'Ä…': 'a', 'Ä‡': 'c', 'Ä™': 'e', 'Å‚': 'l', 'Å„': 'n', 'Ã³': 'o', 'Å›': 's',
        'Åº': 'z', 'Å¼': 'z',
        'Ä„': 'A', 'Ä†': 'C', 'Ä˜': 'E', 'Å': 'L', 'Åƒ': 'N', 'Ã“': 'O', 'Åš': 'S',
        'Å¹': 'Z', 'Å»': 'Z'
    };
    var LATVIAN_MAP = {
        'Ä': 'a', 'Ä': 'c', 'Ä“': 'e', 'Ä£': 'g', 'Ä«': 'i', 'Ä·': 'k', 'Ä¼': 'l',
        'Å†': 'n', 'Å¡': 's', 'Å«': 'u', 'Å¾': 'z',
        'Ä€': 'A', 'ÄŒ': 'C', 'Ä’': 'E', 'Ä¢': 'G', 'Äª': 'I', 'Ä¶': 'K', 'Ä»': 'L',
        'Å…': 'N', 'Å ': 'S', 'Åª': 'U', 'Å½': 'Z'
    };
    var ARABIC_MAP = {
        'Ø£': 'a', 'Ø¨': 'b', 'Øª': 't', 'Ø«': 'th', 'Ø¬': 'g', 'Ø­': 'h', 'Ø®': 'kh', 'Ø¯': 'd',
        'Ø°': 'th', 'Ø±': 'r', 'Ø²': 'z', 'Ø³': 's', 'Ø´': 'sh', 'Øµ': 's', 'Ø¶': 'd', 'Ø·': 't',
        'Ø¸': 'th', 'Ø¹': 'aa', 'Øº': 'gh', 'Ù': 'f', 'Ù‚': 'k', 'Ùƒ': 'k', 'Ù„': 'l', 'Ù…': 'm',
        'Ù†': 'n', 'Ù‡': 'h', 'Ùˆ': 'o', 'ÙŠ': 'y'
    };
    var LITHUANIAN_MAP = {
        'Ä…': 'a', 'Ä': 'c', 'Ä™': 'e', 'Ä—': 'e', 'Ä¯': 'i', 'Å¡': 's', 'Å³': 'u',
        'Å«': 'u', 'Å¾': 'z',
        'Ä„': 'A', 'ÄŒ': 'C', 'Ä˜': 'E', 'Ä–': 'E', 'Ä®': 'I', 'Å ': 'S', 'Å²': 'U',
        'Åª': 'U', 'Å½': 'Z'
    };
    var SERBIAN_MAP = {
        'Ñ’': 'dj', 'Ñ˜': 'j', 'Ñ™': 'lj', 'Ñš': 'nj', 'Ñ›': 'c', 'ÑŸ': 'dz',
        'Ä‘': 'dj', 'Ð‚': 'Dj', 'Ðˆ': 'j', 'Ð‰': 'Lj', 'ÐŠ': 'Nj', 'Ð‹': 'C',
        'Ð': 'Dz', 'Ä': 'Dj'
    };
    var AZERBAIJANI_MAP = {
        'Ã§': 'c', 'É™': 'e', 'ÄŸ': 'g', 'Ä±': 'i', 'Ã¶': 'o', 'ÅŸ': 's', 'Ã¼': 'u',
        'Ã‡': 'C', 'Æ': 'E', 'Äž': 'G', 'Ä°': 'I', 'Ã–': 'O', 'Åž': 'S', 'Ãœ': 'U'
    };
    var GEORGIAN_MAP = {
        'áƒ': 'a', 'áƒ‘': 'b', 'áƒ’': 'g', 'áƒ“': 'd', 'áƒ”': 'e', 'áƒ•': 'v', 'áƒ–': 'z',
        'áƒ—': 't', 'áƒ˜': 'i', 'áƒ™': 'k', 'áƒš': 'l', 'áƒ›': 'm', 'áƒœ': 'n', 'áƒ': 'o',
        'áƒž': 'p', 'áƒŸ': 'j', 'áƒ ': 'r', 'áƒ¡': 's', 'áƒ¢': 't', 'áƒ£': 'u', 'áƒ¤': 'f',
        'áƒ¥': 'q', 'áƒ¦': 'g', 'áƒ§': 'y', 'áƒ¨': 'sh', 'áƒ©': 'ch', 'áƒª': 'c', 'áƒ«': 'dz',
        'áƒ¬': 'w', 'áƒ­': 'ch', 'áƒ®': 'x', 'áƒ¯': 'j', 'áƒ°': 'h'
    };

    var ALL_DOWNCODE_MAPS = [
        LATIN_MAP,
        LATIN_SYMBOLS_MAP,
        GREEK_MAP,
        TURKISH_MAP,
        ROMANIAN_MAP,
        RUSSIAN_MAP,
        UKRAINIAN_MAP,
        CZECH_MAP,
        POLISH_MAP,
        LATVIAN_MAP,
        ARABIC_MAP,
        LITHUANIAN_MAP,
        SERBIAN_MAP,
        AZERBAIJANI_MAP,
        GEORGIAN_MAP
    ];

    var Downcoder = {
        'Initialize': function() {
            if (Downcoder.map) {  // already made
                return;
            }
            Downcoder.map = {};
            Downcoder.chars = [];
            for (var i = 0; i < ALL_DOWNCODE_MAPS.length; i++) {
                var lookup = ALL_DOWNCODE_MAPS[i];
                for (var c in lookup) {
                    if (lookup.hasOwnProperty(c)) {
                        Downcoder.map[c] = lookup[c];
                    }
                }
            }
            for (var k in Downcoder.map) {
                if (Downcoder.map.hasOwnProperty(k)) {
                    Downcoder.chars.push(k);
                }
            }
            Downcoder.regex = new RegExp(Downcoder.chars.join('|'), 'g');
        }
    };

    function downcode(slug) {
        Downcoder.Initialize();
        return slug.replace(Downcoder.regex, function(m) {
            return Downcoder.map[m];
        });
    }


    function URLify(s, num_chars, allowUnicode) {
        // changes, e.g., "Petty theft" to "petty-theft"
        // remove all these words from the string before urlifying
        if (!allowUnicode) {
            s = downcode(s);
        }

        /*
        THIS IS THE PATCHED PART! We removed all the words and thus preserve
        any "and", "the", "an" etc. in the slug.
        */
        var removelist = [];

        var r = new RegExp('\\b(' + removelist.join('|') + ')\\b', 'gi');
        s = s.replace(r, '');
        // if downcode doesn't hit, the char will be stripped here
        if (allowUnicode) {
            // Keep Unicode letters including both lowercase and uppercase
            // characters, whitespace, and dash; remove other characters.
            s = XRegExp.replace(s, XRegExp('[^-_\\p{L}\\p{N}\\s]', 'g'), '');
        } else {
            s = s.replace(/[^-\w\s]/g, '');  // remove unneeded chars
        }
        s = s.replace(/^\s+|\s+$/g, '');   // trim leading/trailing spaces
        s = s.replace(/[-\s]+/g, '-');     // convert spaces to hyphens
        s = s.toLowerCase();               // convert to lowercase
        return s.substring(0, num_chars);  // trim to first num_chars chars
    }
    window.URLify = URLify;
})();
