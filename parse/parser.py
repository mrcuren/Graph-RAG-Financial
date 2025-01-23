from pathlib import Path
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
    TesseractCliOcrOptions,
)
from docling.document_converter import DocumentConverter, PdfFormatOption
import logging

# Loglama ayarları
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Pipeline options ayarları
pipeline_options = PdfPipelineOptions()
pipeline_options.do_ocr = True
pipeline_options.do_table_structure = True
pipeline_options.table_structure_options.do_cell_matching = True

ocr_options = TesseractCliOcrOptions(force_full_page_ocr=False)
pipeline_options.ocr_options = ocr_options

converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(
            pipeline_options=pipeline_options
        )
    }
)

# Data klasöründeki tüm PDF dosyalarını işlemek
data_folder = Path("/home/mericuren/Desktop/graph_Rag/data")
pdf_files = data_folder.glob("*.pdf")

for pdf_file in pdf_files:
    markdown_file = data_folder / f"{pdf_file.stem}.md"

    # Eğer .md dosyası zaten varsa es geç ve logla
    if markdown_file.exists():
        logger.info(f"Markdown file already exists: {markdown_file}. Skipping...")
        continue

    try:
        logger.info(f"Processing PDF file: {pdf_file}")

        # PDF'yi dönüştür ve Markdown olarak kaydet
        doc = converter.convert(pdf_file).document
        md = doc.export_to_markdown()

        with open(markdown_file, "w", encoding="utf-8") as f:
            f.write(md)

        logger.info(f"Successfully processed and saved: {markdown_file}")

    except Exception as e:
        logger.error(f"Error processing {pdf_file}: {e}", exc_info=True)