document.addEventListener("DOMContentLoaded", function() {
  const browseBtn = document.getElementById("browse-btn");
  const addBtn = document.getElementById("add-btn");
  const contentBlock = document.querySelector(".content");

  browseBtn.addEventListener("click", async () => {
    contentBlock.innerHTML = "";
    const response = await fetch("/exoplanets/");
    const exoplanets = await response.json();

    const exoplanetList = document.createElement("ul");

    exoplanets.forEach(exoplanet => {
      const listItem = document.createElement("li");
      listItem.textContent = exoplanet.planet_name;
      exoplanetList.appendChild(listItem);
    });

    contentBlock.appendChild(exoplanetList);
  });

  addBtn.addEventListener("click", () => {
    contentBlock.innerHTML = "";
    const form = createExoplanetForm();
    contentBlock.appendChild(form);

    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const formData = new FormData(form);
      const exoplanetData = Object.fromEntries(formData);

      const response = await fetch("/exoplanets/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify(exoplanetData),
      });

      if (response.ok) {
        alert("Exoplanet added successfully!");
        form.reset();
      } else {
        alert("Error adding exoplanet. Please try again.");
      }
    });
  });
});


function createExoplanetForm() {
  const form = document.createElement("form");
  form.setAttribute("id", "exoplanet-form");

  const fields = [
    { name: "planet_name", label: "Planet Name", type: "text" },
    { name: "star_name", label: "Star Name", type: "text" },
    { name: "habitability", label: "Habitability", type: "select", options: [["NH", "Non Habitable"], ["OH", "Optimistically Habitable"], ["CH", "Conservatively Habitable"]] },
    { name: "planet_radius", label: "Planet Radius", type: "number" },
    { name: "planet_period", label: "Planet Period", type: "number" },
    { name: "planet_temperature_equilibrium", label: "Planet Equilibrium Temperature", type: "number" },
    { name: "planet_temperature_equilibrium_min", label: "Planet Min Equilibrium Temperature", type: "number" },
    { name: "planet_temperature_equilibrium_max", label: "Planet Max Equilibrium Temperature ", type: "number" },
    { name: "distance_to_star", label: "Distance to Star", type: "number" },
    { name: "star_mass", label: "Star Mass", type: "number" },
    { name: "star_radius", label: "Star Radius", type: "number" },
    { name: "star_temperature", label: "Star Temperature", type: "number" },
    { name: "star_luminosity", label: "Star Luminosity", type: "number" },
    { name: "star_metallicity", label: "Star Metallicity", type: "number" },
  ];

  fields.forEach(field => {
    const label = document.createElement("label");
    label.setAttribute("for", field.name);
    label.textContent = field.label;
    form.appendChild(label);

    if (field.type === "select") {
      const select = document.createElement("select");
      select.setAttribute("name", field.name);
      select.setAttribute("id", field.name);
      field.options.forEach(option => {
        const opt = document.createElement("option");
        opt.setAttribute("value", option[0]);
        opt.textContent = option[1];
        select.appendChild(opt);
      });
      form.appendChild(select);
    } else {
      const input = document.createElement("input");
      input.setAttribute("type", field.type);
      input.setAttribute("name", field.name);
      input.setAttribute("id", field.name);
      form.appendChild(input);
    }
    form.appendChild(document.createElement("br"));
  });

  const submitBtn = document.createElement("button");
  submitBtn.setAttribute("type", "submit");
  submitBtn.textContent = "Add Exoplanet";
  form.appendChild(submitBtn);

  return form;
}