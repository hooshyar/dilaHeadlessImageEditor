# Google Fonts Integration

The Dila Headless Image Editor now supports Google Fonts, allowing you to use any free Google Font in your text overlays without needing to install them locally.

## How It Works

1. When you specify a Google Font in your API request, the font is automatically downloaded and cached for future use.
2. The font is stored in the `fonts/google_fonts` directory and will be reused for subsequent requests.
3. You can specify font weights and styles in addition to the font family.

## Usage

### Specifying a Google Font

To use a Google Font, simply specify the font name in the `font_family` parameter of your API request:

```json
{
  "font_family": "Roboto"
}
```

### Specifying Font Weight

You can specify a font weight by adding a colon and the weight number:

```json
{
  "font_family": "Roboto:700"  // Bold Roboto
}
```

Common weights include:
- 100 (Thin)
- 300 (Light)
- 400 (Regular, default)
- 500 (Medium)
- 700 (Bold)
- 900 (Black/Extra Bold)

### Specifying Font Style

You can specify italic style:

```json
{
  "font_family": "Roboto:italic"  // Italic Roboto
}
```

### Combining Weight and Style

You can combine weight and style:

```json
{
  "font_family": "Roboto:700italic"  // Bold Italic Roboto
}
```

## Arabic/Kurdish Font Recommendations

For Arabic and Kurdish text, we recommend the following Google Fonts that have excellent RTL language support:

- `Noto Sans Arabic` - A comprehensive font with excellent Unicode support
- `Cairo` - Modern, clean design with good readability
- `Tajawal` - Elegant design with multiple weights
- `Almarai` - Contemporary design with excellent readability
- `Amiri` - Traditional style, good for formal contexts
- `Scheherazade New` - Traditional Naskh style with excellent readability

Example:

```json
{
  "font_family": "Cairo:700",  
  "text": "مرحبا بالعالم", 
  "language": "ar"
}
```

## Getting Available Fonts

You can retrieve a list of available fonts (both local and popular Google Fonts) using the `/fonts` endpoint:

```
GET http://localhost:5001/fonts
```

The response will include:
- `local_fonts`: Array of fonts available locally
- `popular_google_fonts`: Array of recommended Google Fonts that work well with the image editor

## Caching

Downloaded Google Fonts are cached in the `fonts/google_fonts` directory to improve performance and reduce bandwidth usage. The cache is persistent across server restarts.

## Fallback Mechanism

If a requested Google Font cannot be downloaded for any reason, the system will automatically fall back to a suitable local font to ensure text is always rendered.

## Technical Implementation

The Google Fonts integration uses the Google Fonts CSS2 API, which doesn't require an API key for basic usage. Fonts are downloaded in TTF format for maximum compatibility with the Pillow image processing library. 