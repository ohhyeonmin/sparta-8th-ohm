console.log(1+1);
console.log(1-2);
console.log(2*3);
console.log(3/4);
console.log("나는" + "학생입니다.");

var a1=1;
let a2=2;
const a3=3;

//array 
let a4=[];
a4.push('A');
console.log(a4);

//object (이해안됨)
let a5 ={
    test: 123
}
console.log(a5['test']);
const {test} =a5;
console.log(test);

// 반복 (이해안됨)
let b = [1, 2, 3, 4, 5];

b = b.map(function(i) {

  return i * 3

});

// console.log(b);

let b1 = [1, 2, 3, 4, 5];
b1 = b1.filter(function(i) {
  return i < 4;
});
// console.log(b1);

// 누적기

let b2 = [1, 2, 3, 4, 5];
let sum = b2.reduce(function(acc, cur) {
  // acc는 지금까지 누적된 합산 결과
  // cur는 지금 현재 값
  return acc + cur;
});
//  1 + 2 + 3 + 4 + 5

