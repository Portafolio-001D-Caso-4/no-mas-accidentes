!function($) {
    "use strict";

    var CalendarPage = function() {};

    CalendarPage.prototype.init = function() {
            var addEvent=$("#event-modal");
            var modalTitle = $("#modal-title");
            var formEvent = $("#form-event");
            var selectedEvent = null;
            var newEventData = null;
            var forms = document.getElementsByClassName('needs-validation');
            var selectedEvent = null;
            var newEventData = null;
            var eventObject = null;
            /* initialize the calendar */


            var calendarEl = document.getElementById('calendar');

            // function addNewEvent(info) {
            //     addEvent.modal('show');
            //     formEvent.removeClass("was-validated");
            //     formEvent[0].reset();
            //
            //     $("#event-title").val();
            //     $('#event-category').val();
            //     modalTitle.text('Add Event');
            //     newEventData = info;
            // }


            var calendar = new FullCalendar.Calendar(calendarEl, {
                plugins: [ 'bootstrap', 'interaction', 'dayGrid', 'timeGrid'],
                editable: false,
                droppable: false,
                selectable: true,
                defaultView: 'dayGridMonth',
                themeSystem: 'bootstrap',
                header: {
                    left: 'prev,next today',
                    center: 'title',
                    right: 'dayGridMonth,timeGridWeek,timeGridDay,listMonth'
                },
                dayNames: ['Domingo', 'Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado'],
                dayNamesShort: ['Dom','Lun','Mar','Mie','Jue','Vie','Sáb'],
                monthNamesShort: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
                monthNames: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
                buttonText: {
                    today:    'Hoy',
                    month:    'Mes',
                    week:     'Semana',
                    day:      'Día',
                    list:     'Lista'
                },
                eventTimeFormat: {
                    hour: '2-digit',
                    minute: '2-digit',
                    meridiem: false
                },
                eventClick: function(info) {
                    addEvent.modal('show');
                    formEvent[0].reset();
                    selectedEvent = info.event;
                    $("#event-title").val(selectedEvent.title);
                    $('#event-category').val(selectedEvent.classNames[0]);
                    $("#event-profesional").val(selectedEvent.extendedProps.profesionalAsignado);
                    $("#event-empresa").val(selectedEvent.extendedProps.empresa);
                    $("#event-desde").val(selectedEvent.start.toLocaleString("es-ES"));
                    $("#event-hasta").val(selectedEvent.end.toLocaleString("es-ES"));
                    $("#event-url").prop('href', selectedEvent.extendedProps.urlEvento);
                    $("#event-title").prop('disabled', true);
                    $('#event-category').prop('disabled', true);
                    $("#event-profesional").prop('disabled', true);
                    $("#event-empresa").prop('disabled', true);
                    $("#event-desde").prop('disabled', true);
                    $("#event-hasta").prop('disabled', true);


                    newEventData = null;
                    modalTitle.text('Evento agendado');
                    newEventData = null;
                },
                dateClick: function(info) {
                    addNewEvent(info);
                },
                events : defaultEvents
            });
            calendar.render();

             /*Add new event*/
            // Form to add new event

            $(formEvent).on('submit', function(ev) {
                ev.preventDefault();
                var inputs = $('#form-event :input');
                var updatedTitle = $("#event-title").val();
                var updatedCategory =  $('#event-category').val();

                // validation
                if (forms[0].checkValidity() === false) {
                        event.preventDefault();
                        event.stopPropagation();
                        forms[0].classList.add('was-validated');
                } else {
                    if(selectedEvent){
                        selectedEvent.setProp("title", updatedTitle);
                        selectedEvent.setProp("classNames", [updatedCategory]);
                    } else {
                        var newEvent = {
                            title: updatedTitle,
                            start: newEventData.date,
                            allDay: newEventData.allDay,
                            className: updatedCategory
                        }
                        calendar.addEvent(newEvent);
                    }
                    addEvent.modal('hide');
                }
            });


    },
    //init
    $.CalendarPage = new CalendarPage, $.CalendarPage.Constructor = CalendarPage
}(window.jQuery),

//initializing
function($) {
    "use strict";
    $.CalendarPage.init()
}(window.jQuery);
