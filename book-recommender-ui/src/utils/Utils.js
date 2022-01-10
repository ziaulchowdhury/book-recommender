
export default function getLanguageName(langCode) {
    const languageNames = new Intl.DisplayNames(['en'], {
        type: 'language'
    });
    return  languageNames.of(langCode);
}