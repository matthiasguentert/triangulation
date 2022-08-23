import freetype

face = freetype.Face("C:\Windows\Fonts\Arial.ttf")
face.set_char_size(48*64)
face.load_char('S')
bitmap = face.glyph.bitmap
