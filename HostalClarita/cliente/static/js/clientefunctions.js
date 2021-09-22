$(document).ready( function () {

    //Tabla de habitaciones ingreso manual
    $('#tablaSltHabis').DataTable({
        language: {
            url: 'https://cdn.datatables.net/plug-ins/1.10.25/i18n/Spanish.json'
        },
        dom: 'Bfrtip',
        buttons: [
           
        ],
        pageLength: 4,

    
    });

    //Tabla de menú semanal
    $('#menuSemanal').DataTable({
        language: {
            url: 'https://cdn.datatables.net/plug-ins/1.10.25/i18n/Spanish.json'
        },
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ],
        initComplete: function () {
            var btns = $('.dt-button');
            btns.addClass('btn btn-warning btn-sm');
            btns.removeClass('dt-button');
        }

    });

    //Tabla de habitaciones ingreso planilla
    $('#tablalstHabis').DataTable({
        language: {
            url: 'https://cdn.datatables.net/plug-ins/1.10.25/i18n/Spanish.json'
        },
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ],
        initComplete: function () {
            var btns = $('.dt-button');
            btns.addClass('btn btn-warning btn-sm');
            btns.removeClass('dt-button');
        },
        pageLength: 5,
    });

    //Tabla de huespedes ingreso planilla
    $('#tablaHuespPlani').DataTable({
        language: {
            url: 'https://cdn.datatables.net/plug-ins/1.10.25/i18n/Spanish.json'
        },
        dom: 'Bfrtip',
        buttons: [
        ],
        pageLength: 5,
    });

    //Tabla de huespedes ingreso manual
    $('#tablaHuespManual').DataTable({
        language: {
            url: 'https://cdn.datatables.net/plug-ins/1.10.25/i18n/Spanish.json'
        },
        dom: 'Bfrtip',
        buttons: [
        ],
        pageLength: 5,
    });


       $('#tblClienteCompras').DataTable({
        language: {
            url: 'https://cdn.datatables.net/plug-ins/1.10.25/i18n/Spanish.json'
        },
        dom: 'Bfrtip',
        buttons: [
            { 
                extend: 'copy',
                exportOptions: {
                columns: [ 0, 1, 2 ]
            }},
            { 
                extend: 'csv',
                exportOptions: {
                columns: [ 0, 1, 2 ]
            } },
            { 
                extend: 'excel',
                exportOptions: {
                columns: [ 0, 1, 2 ]
            } },
            { 
                extend: 'pdf',
                exportOptions: {
                columns: [ 0, 1, 2 ]
            } },
            { 
                extend: 'print',
                exportOptions: {
                columns: [ 0, 1, 2 ]
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


