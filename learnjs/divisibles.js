const prompt = require("prompt-sync")();

function enterNumber() {
    let number = prompt("Write a number");
    if (number !== null && !isNaN(number) && number > 0) {
        return parseInt(number);
    } else {
        console.log("Please enter a valid positive number");
        return enterNumber();
    }
}

function crearLista() {
    let number = enterNumber();
    let lista = []
    for (let i = 1; i <= number; i++) {
        if (i % 3 === 0 && i % 5 === 0) {
            lista.push("foobar")
        } else if (i % 3 === 0) {
            lista.push("foo")
        } else if (i % 5 === 0) {
            lista.push("bar")
        } else {
            lista.push(i);
        }
    }
    return lista;
}

console.log(crearLista());