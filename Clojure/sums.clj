;;
;; Small demo for summing up - just for fun; of course Gauß exists!
;;
(ns mysums
  (:use clojure.test))

;
; simple recursive solution
;
(defn sum [n]
  (loop [acc 0 rest n]
    (if (zero? rest)
      acc
      (recur (+ acc rest) (dec rest)))))

;
; using reduce
;
(defn sum-reduce [n]
  (reduce + (range 1 (+ n 1))))

;;
;; Testing
;;
(deftest test-recursive-sum
  (is (= 0 (sum 0)))
  (is (= 1 (sum 1)))
  (is (= 15 (sum 5))))

(deftest test-sum-reduce
  (is (= 0 (sum-reduce 0)))
  (is (= 1 (sum-reduce 1)))
  (is (= 15 (sum-reduce 5))))

(run-tests 'mysums)
