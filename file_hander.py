import csv
import io
import re
import zipfile

import chardet
from opencc import OpenCC


TXT_FILE_EXTENSIONS = {'opf', 'ncx', 'xml', 'xhtml', 'html', 'htm', 'txt'}

converters = [OpenCC("t2tw.json"), OpenCC("tw2sp.json")]


async def convert(text: str, substitution_dict: dict[str, str]) -> str:
    for converter in converters:
        text = converter.convert(text)
    for pattern, repl in substitution_dict.items():
        text = re.sub(pattern, repl, text)
    return text

async def processor(file: bytes, title: str) -> tuple[bytes, str]:
    substitution_dict = {row[0]: row[1] for row in csv.reader(open('substitutions.csv', encoding='utf-8')) if len(row) >= 2}
    title = await convert(title, substitution_dict)
    output_buffer = io.BytesIO()

    try:
        with zipfile.ZipFile(io.BytesIO(file), 'r') as zin, zipfile.ZipFile(output_buffer, 'w') as zout:
            for info in zin.infolist():
                if not info.filename.split('.')[-1].lower() in TXT_FILE_EXTENSIONS:
                    zout.writestr(info.filename, zin.read(info.filename))
                    continue

                text = zin.read(info.filename).decode('utf-8')
                text = await convert(text, substitution_dict)
                zout.writestr(info.filename, text.encode('utf-8'))
    except zipfile.BadZipFile:
        text = file.decode(chardet.detect(file)['encoding'] or 'utf-8')
        text = await convert(text, substitution_dict)
        output_buffer.write(text.encode('utf-8'))

    return output_buffer.getvalue(), title
