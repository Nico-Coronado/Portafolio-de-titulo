$(document).ready( function () {

    //Tabla de Cesta
    $('#tablaCesta').DataTable({
        language: {
            url: 'https://cdn.datatables.net/plug-ins/1.10.25/i18n/Spanish.json'
        },
        dom: 'Bfrtip',
        buttons: [
           
        ],
    
    });

   //Tabla para mostrar pedido
   $('#tablaPediNuevo').DataTable({
        language: {
            url: 'https://cdn.datatables.net/plug-ins/1.10.25/i18n/Spanish.json'
        },
        dom: 'Bfrtip',
        buttons: [
        
        ],

    });

//Tabla para mostrar pedido
   $('#tablaPediMostrar').DataTable({
        language: {
            url: 'https://cdn.datatables.net/plug-ins/1.10.25/i18n/Spanish.json'
        },
        dom: 'Bfrtip',
        buttons: [
        
        ],

    });


    //Tabla de productos de proveedor:
    $('#tablaMercado').DataTable({       
            language: {
                url: 'https://cdn.datatables.net/plug-ins/1.10.25/i18n/Spanish.json'
            },
            dom: 'Bfrtip',
            buttons: [
                { 
                    extend: 'copy',
                    exportOptions: {
                    columns: [ 0, 1, 2,3,4,5 ]
                }},
                { 
                    extend: 'csv',
                    exportOptions: {
                    columns: [ 0, 1, 2,3,4,5 ]
                } },
                { 
                    extend: 'excel',
                    exportOptions: {
                    columns: [ 0, 1, 2,3,4,5 ]
                } },
                { 
                    extend: 'pdf',
                    exportOptions: {
                    columns: [ 0, 1, 2,3,4,5 ]
                } },
                { 
                    extend: 'print',
                    exportOptions: {
                    columns: [ 0, 1, 2,3,4,5 ]
                } 
            }
            ],
            initComplete: function () {
                var btns = $('.dt-button');
                btns.addClass('btn btn-info btn-sm');
                btns.removeClass('dt-button');
            }

        });   

    //Tabla de pedidos creados
    $('#tbPediCreados').DataTable({
        language: {
            url: 'https://cdn.datatables.net/plug-ins/1.10.25/i18n/Spanish.json'
        },
        dom: 'Bfrtip',
        buttons: [
           
        ],
    
    });
    //Tabla de pedidos pendientes
    $('#tbPediPendientes').DataTable({
        language: {
            url: 'https://cdn.datatables.net/plug-ins/1.10.25/i18n/Spanish.json'
        },
        dom: 'Bfrtip',
        buttons: [
        
        ],

    });

    //Tabla de pedidos por revisar
    $('#tbPediRevisar').DataTable({
        language: {
            url: 'https://cdn.datatables.net/plug-ins/1.10.25/i18n/Spanish.json'
        },
        dom: 'Bfrtip',
        buttons: [
        
        ],

    });


//HISTORIAL PEDIDOS
    //Tabla de pedidos aceptados
    $('#tablaPediAceptados').DataTable({
        language: {
            url: 'https://cdn.datatables.net/plug-ins/1.10.25/i18n/Spanish.json'
        },
        dom: 'Bfrtip',
        buttons: [
            { 
                extend: 'copy',
                exportOptions: {
                columns: [ 0, 1, 2,3,4,5 ]
            }},
            { 
                extend: 'csv',
                exportOptions: {
                columns: [ 0, 1, 2,3,4,5 ]
            } },
            { 
                extend: 'excel',
                exportOptions: {
                columns: [ 0, 1, 2,3,4,5 ]
            } },
            { 
                extend: 'pdf',
                exportOptions: {
                columns: [ 0, 1, 2,3,4,5 ]
            } },
            { 
                extend: 'print',
                exportOptions: {
                columns: [ 0, 1, 2,3,4,5 ]
            } 
        }
        ],
        initComplete: function () {
            var btns = $('.dt-button');
            btns.addClass('btn btn-success btn-sm');
            btns.removeClass('dt-button');
        }

    });

    //Tabla de pedidos por recepcionas
    $('#tablaPediRecep').DataTable({
        language: {
            url: 'https://cdn.datatables.net/plug-ins/1.10.25/i18n/Spanish.json'
        },
        dom: 'Bfrtip',
        buttons: [
            { 
                extend: 'copy',
                exportOptions: {
                columns: [ 0, 1, 2,3,4,5 ]
            }},
            { 
                extend: 'csv',
                exportOptions: {
                columns: [ 0, 1, 2,3,4,5 ]
            } },
            { 
                extend: 'excel',
                exportOptions: {
                columns: [ 0, 1, 2,3,4,5 ]
            } },
            { 
                extend: 'pdf',
                exportOptions: {
                columns: [ 0, 1, 2,3,4,5 ]
            } },
            { 
                extend: 'print',
                exportOptions: {
                columns: [ 0, 1, 2,3,4,5 ]
            } 
        }
        ],
        initComplete: function () {
            var btns = $('.dt-button');
            btns.addClass('btn btn-warning btn-sm');
            btns.removeClass('dt-button');
        }

    });

        //Tabla de pedidos cancelados
        $('#tablaPediCancel').DataTable({
            language: {
                url: 'https://cdn.datatables.net/plug-ins/1.10.25/i18n/Spanish.json'
            },
            dom: 'Bfrtip',
            buttons: [
                { 
                    extend: 'copy',
                    exportOptions: {
                    columns: [ 0, 1, 2,3,4,5 ]
                }},
                { 
                    extend: 'csv',
                    exportOptions: {
                    columns: [ 0, 1, 2,3,4,5 ]
                } },
                { 
                    extend: 'excel',
                    exportOptions: {
                    columns: [ 0, 1, 2,3,4,5 ]
                } },
                { 
                    extend: 'pdf',
                    exportOptions: {
                    columns: [ 0, 1, 2,3,4,5 ]
                } },
                { 
                    extend: 'print',
                    exportOptions: {
                    columns: [ 0, 1, 2,3,4,5 ]
                } 
            }
            ],
            initComplete: function () {
                var btns = $('.dt-button');
                btns.addClass('btn btn-info btn-sm');
                btns.removeClass('dt-button');
            }
    
        });

        //Tabla de pedidos rechazados
        $('#tablaPediRechaz').DataTable({
            language: {
                url: 'https://cdn.datatables.net/plug-ins/1.10.25/i18n/Spanish.json'
            },
            dom: 'Bfrtip',
            buttons: [
                { 
                    extend: 'copy',
                    exportOptions: {
                    columns: [ 0, 1, 2,3,4,5 ]
                }},
                { 
                    extend: 'csv',
                    exportOptions: {
                    columns: [ 0, 1, 2,3,4,5 ]
                } },
                { 
                    extend: 'excel',
                    exportOptions: {
                    columns: [ 0, 1, 2,3,4,5 ]
                } },
                { 
                    extend: 'pdf',
                    exportOptions: {
                    columns: [ 0, 1, 2,3,4,5 ]
                } },
                { 
                    extend: 'print',
                    exportOptions: {
                    columns: [ 0, 1, 2,3,4,5 ]
                } 
            }
            ],
            initComplete: function () {
                var btns = $('.dt-button');
                btns.addClass('btn btn-primary btn-sm');
                btns.removeClass('dt-button');
            }
    
        });

} );


