const loadCalendar = () => {
  const calendarEl = document.getElementById("calendar");

  const calendar = new FullCalendar.Calendar(calendarEl, {
    themeSystem: "bootstrap5",
    firstDay: 1,
    // initialDate: firstDayOfNextMonth(),
    locale: "ru",
    timeZone: "Europe/Moscow",
    dayMaxEvents: true,
    editable: true,
    eventDurationEditable: false,
    eventStartEditable: true,
    selectable: true,
    headerToolbar: {
      start: "",
      center: "title",
      end: "prev,next",
    },
    events: "/api/v1/schedules/get_calendar",
    eventDrop: patchSchedulesDate,
    eventDidMount: createPopoversWithSchdules,
  });

  calendar.render();
};

const firstDayOfNextMonth = () => {
  const date = new Date();
  return new Date(date.getFullYear(), date.getMonth() + 2, 1);
};

const createPopoversWithSchdules = async (info) => {
  const schedulesData = info.event.extendedProps.schedules;
  const options = {
    html: true,
    sanitize: false,
    placement: "auto",
    title: info.event.title,
    trigger: "hover",
    content: renderSchedulesTable(schedulesData),
  };
  const popover = new bootstrap.Popover(info.el, options);
};

const renderSchedulesTable = (schedules) => {
  let trElements = "";
  schedules.forEach((element) => {
    trElements += `<tr><td>${element.maintenance_type}</td><td>${element.equipment_type}</td</tr>`;
  });
  return `<table class="table table-sm"><tbody>${trElements}</tbody></table>`;
};

const patchSchedulesDate = async (info) => {
  if (isDateInPast(info)) {
    return;
  }
  const schedulesData = info.event.extendedProps.schedules;
  const payload = {
    date_sheduled: info.event.start.toJSON().substring(0, 10),
    schedules: schedulesData,
  };
  const fetchOptions = {
    method: "POST",
    credentials: "same-origin",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  };

  fetch("/api/v1/schedules/bulk_update/", fetchOptions)
    .then((response) => {
      if (response.status != 200) {
        info.revert();
        alert(
          "Что-то пошло не так! Обновите страницу и обратитесь к администратору. Возможно, выполненные изменения будут потеряны"
        );
        return;
      }
    })
    .catch((error) => console.log("Error", error));
};

const isDateInPast = (info) => {
  const currentDate = new Date();
  currentDate.setDate(currentDate.getDate() - 1);
  if (currentDate > info.event.start) {
    alert("Нельзя запланировать работу на прошлое!");
    info.revert();
    return true;
  }
  return false;
};
