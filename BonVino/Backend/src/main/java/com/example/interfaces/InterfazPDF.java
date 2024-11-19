package com.example.interfaces;

import java.io.IOException;
import java.util.List;

import com.itextpdf.io.image.ImageDataFactory;
import com.itextpdf.kernel.colors.ColorConstants;
import com.itextpdf.kernel.pdf.PdfDocument;
import com.itextpdf.kernel.pdf.PdfWriter;
import com.itextpdf.layout.Document;
import com.itextpdf.layout.element.Image;
import com.itextpdf.layout.element.Paragraph;
import com.itextpdf.layout.element.Table;
import com.itextpdf.layout.element.Cell;
import com.itextpdf.layout.properties.HorizontalAlignment;
import com.itextpdf.layout.properties.TextAlignment;
import com.itextpdf.layout.properties.UnitValue;
import org.springframework.stereotype.Component;

@Component
public class InterfazPDF {

    // Método para crear el PDF a partir de una lista de resultados
    public void exportarPDF(List<String[]> datos) throws IOException {

        String nombreArchivo = "ReporteRankingVinos.pdf";
        PdfDocument pdf = new PdfDocument(new PdfWriter(nombreArchivo));
        Document document = new Document(pdf);

        // Crear tabla con encabezados
        Table table = new Table(new float[]{1, 1, 1, 1, 1, 1, 1});

        // Estilo de encabezados
        table.addHeaderCell(new Cell().add(new Paragraph("Nombre")).setBackgroundColor(ColorConstants.RED).setBold());
        table.addHeaderCell(new Cell().add(new Paragraph("Calificación")).setBackgroundColor(ColorConstants.RED).setBold());
        table.addHeaderCell(new Cell().add(new Paragraph("Precio Sugerido")).setBackgroundColor(ColorConstants.RED).setBold());
        table.addHeaderCell(new Cell().add(new Paragraph("Nombre Bodega")).setBackgroundColor(ColorConstants.RED).setBold());
        table.addHeaderCell(new Cell().add(new Paragraph("Varietal")).setBackgroundColor(ColorConstants.RED).setBold());
        table.addHeaderCell(new Cell().add(new Paragraph("Región")).setBackgroundColor(ColorConstants.RED).setBold());
        table.addHeaderCell(new Cell().add(new Paragraph("País")).setBackgroundColor(ColorConstants.RED).setBold());

        // Llenar los datos
        for (String[] infoVino : datos) {
            for (String info : infoVino) {
                table.addCell(new Cell().add(new Paragraph(info)).setTextAlignment(TextAlignment.CENTER).setPadding(3));
            }
        }

        // Estilo de la tabla
        table.setWidth(UnitValue.createPercentValue(100)); // Ajustar el ancho de la tabla
        table.setHorizontalAlignment(HorizontalAlignment.CENTER);
        table.setMarginTop(10);
        table.setMarginBottom(10);

        document.add(table);
        document.close();

        System.out.println("PDF creado exitosamente en: " + nombreArchivo);
    }
}