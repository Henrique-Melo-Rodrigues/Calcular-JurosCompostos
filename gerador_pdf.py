from pyscript import window

def exportar_para_pdf(element_id):
    window.eval(f"""
        const gerarPDF = () => {{
            const elemento = document.getElementById('{element_id}');

            elemento.classList.add('pdf-mode');

            const dataAtual = new Date().toLocaleDateString('pt-BR', {{
                day: '2-digit', month: '2-digit', year: 'numeric',
                hour: '2-digit', minute: '2-digit'
            }});
            const dataEl = document.createElement('p');
            dataEl.id = 'pdf-data-geracao';
            dataEl.style.cssText = 'font-size:0.8rem;color:#647469;margin:0 0 8px;';
            dataEl.textContent = 'Gerado em: ' + dataAtual;
            elemento.insertBefore(dataEl, elemento.firstChild);

            const style = document.createElement('style');
            style.id = 'pdf-temp-style';
            style.textContent = `
                .pdf-mode .summary {{
                    gap: 1px;
                }}
                .pdf-mode .summary-card {{
                    min-height: auto;
                    padding: 8px 12px;
                }}
                .pdf-mode .summary-card span {{
                    margin-bottom: 4px;
                    font-size: 0.75rem;
                }}
                .pdf-mode .summary-card strong {{
                    font-size: 1rem;
                }}
                .pdf-mode .table-wrapper {{
                    overflow: visible;
                    width: 100%;
                }}
                .pdf-mode table {{
                    min-width: unset;
                    width: 100%;
                    table-layout: auto;
                    font-size: 0.75rem;
                }}
                .pdf-mode th,
                .pdf-mode td {{
                    padding: 5px 8px;
                    white-space: nowrap;
                }}
            `;
            document.head.appendChild(style);

            /* Largura fixa que garante que a tabela caiba no A4 landscape
               sem depender do tamanho real da janela do usuário.
               A4 landscape a 96 dpi ≈ 1122 px; usamos 1200 para dar margem. */
            const PDF_RENDER_WIDTH = 1200;

            const limpar = () => {{
                elemento.classList.remove('pdf-mode');
                var tempStyle = document.getElementById('pdf-temp-style');
                if (tempStyle) tempStyle.remove();
                var dataGen = document.getElementById('pdf-data-geracao');
                if (dataGen) dataGen.remove();
            }};

            /* Captura manual para poder centralizar o conteúdo no PDF */
            html2canvas(elemento, {{
                scale: 2,
                scrollX: 0,
                scrollY: 0,
                windowWidth: PDF_RENDER_WIDTH,
                width: PDF_RENDER_WIDTH
            }}).then(function(canvas) {{
                /* Dimensões do A4 landscape em mm */
                const pageW = 297;
                const pageH = 210;
                const margin = 5;

                const maxW = pageW - margin * 2;
                const maxH = pageH - margin * 2;

                /* Escala para caber na página mantendo proporção */
                const ratio = canvas.width / canvas.height;
                let imgW = maxW;
                let imgH = imgW / ratio;
                if (imgH > maxH) {{
                    imgH = maxH;
                    imgW = imgH * ratio;
                }}

                /* Centraliza horizontal e verticalmente */
                const x = (pageW - imgW) / 2;
                const y = (pageH - imgH) / 2;

                const imgData = canvas.toDataURL('image/jpeg', 0.98);
                /* O jsPDF UMD expõe como window.jspdf.jsPDF */
                const JsPDF = (window.jspdf && window.jspdf.jsPDF) || window.jsPDF;
                if (!JsPDF) {{
                    console.error('jsPDF não encontrado no window. Verifique se o script foi carregado.');
                    limpar();
                    return;
                }}
                const pdf = new JsPDF({{ unit: 'mm', format: 'a4', orientation: 'landscape' }});
                pdf.addImage(imgData, 'JPEG', x, y, imgW, imgH);
                pdf.save('Calculo-juros-compostos.pdf');

                limpar();
            }}).catch(function(err) {{
                console.error('Erro ao gerar PDF:', err);
                limpar();
            }});
        }};

        gerarPDF()
    """)
