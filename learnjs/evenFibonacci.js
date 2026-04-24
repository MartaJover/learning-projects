function sumEvenFibonacci() {
    let a = 1;
    let b = 2;
    let sum = 0;
    
    if (b <= 4000000) {
        sum += b;
    }
    
    while (a + b <= 4000000) {
        let current = a + b;
        a = b;
        b = current;
        
        if (current % 2 === 0) {
            sum += current;
        }
    }
    
    return sum;
}

console.log(sumEvenFibonacci());