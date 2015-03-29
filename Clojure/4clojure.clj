;; problem 26
;; Fibonacci Sequence
#(loop [n % acc [1 1]]
	(if (> n 2)
		(recur (dec n) (conj acc (apply + (take-last 2 acc))))
		acc))
