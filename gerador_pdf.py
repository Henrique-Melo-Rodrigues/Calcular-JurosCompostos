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
                }}
                .pdf-mode table {{
                    min-width: unset;
                    font-size: 0.8rem;
                }}
                .pdf-mode th,
                .pdf-mode td {{
                    padding: 6px 10px;
                }}
            `;
            document.head.appendChild(style);

            const opcoes = {{
                margin: [5, 5, 5, 5],
                filename: 'Calculo-juros-compostos.pdf',
                image: {{ type: 'jpeg', quality: 0.98 }},
                html2canvas: {{
                    scale: 2,
                    scrollX: 0,
                    scrollY: 0,
                    windowWidth: elemento.scrollWidth
                }},
                jsPDF: {{ unit: 'mm', format: 'a4', orientation: 'landscape' }}
            }};

            html2pdf().set(opcoes).from(elemento).save().then(function() {{
                elemento.classList.remove('pdf-mode');
                var tempStyle = document.getElementById('pdf-temp-style');
                if (tempStyle) tempStyle.remove();
                var dataGen = document.getElementById('pdf-data-geracao');
                if (dataGen) dataGen.remove();
            }});
        }};

        gerarPDF()
    """)
