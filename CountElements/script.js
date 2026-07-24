function count(selector) {
    return document.querySelectorAll(selector).length;
}

const stats = {

    "Total Elements": document.getElementsByTagName("*").length,

    "Tables": count("table"),

    "Rows": count("tr"),

    "Columns": count("td,th"),

    "Images": count("img"),

    "Forms": count("form"),

    "Inputs": count("input"),

    "Buttons": count("button"),

    "Select": count("select"),

    "Textarea": count("textarea"),

    "Links": count("a"),

    "Paragraphs": count("p"),

    "Divs": count("div"),

    "Span": count("span"),

    "Headings": count("h1,h2,h3,h4,h5,h6"),

    "UL": count("ul"),

    "OL": count("ol"),

    "LI": count("li"),

    "HR": count("hr"),

    "IDs": document.querySelectorAll("[id]").length,

    "Classes": document.querySelectorAll("[class]").length,

    "Background Colors": 0,

    "Text Colors": 0
};

// Count elements having background-color or color
document.querySelectorAll("*").forEach(element => {

    const style = getComputedStyle(element);

    if(style.backgroundColor !== "rgba(0, 0, 0, 0)")
        stats["Background Colors"]++;

    if(style.color !== "rgb(0, 0, 0)")
        stats["Text Colors"]++;

});

let output = "";

for(const key in stats){

    output += `${key} : ${stats[key]}\n`;

}

document.getElementById("output").textContent = output;

console.log(stats);