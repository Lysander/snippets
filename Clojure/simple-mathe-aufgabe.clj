;;
;; Lösung zu folgender Aufgabe in Clojure:
;;
;; x % 2 = 1
;; x % 3 = 2
;; x % 4 = 3
;; x % 5 = 4
;; x % 6 = 6
;; x % 7 = 0
;;
;; mit 1 <= x < 1000
;;
(ns simple-math
  (:use clojure.test))

 
(defn make-mod-func [x]
  (partial #(= (mod %2 %1) (- %1 1)) x))
 
(defn make-predicate []
  (apply every-pred
    (cons
      #(zero? (mod % 7))
      (map make-mod-func (range 2 7)))))

(defn solve [limit]
  (filter (make-predicate) (range 1 (+ limit 1))))
  
(solve 1000)
 
;; gibt (119 539 959)

;;
;; Unit Tests
;;
(deftest test-make-func
  (def f (make-mod-func 2))
  (is (true? (f 1)))
  (is (false? (f 2)))
  (is (true? (f 3))))
  
(deftest test-make-predicate
  (def p (make-predicate))
  (is (false? (p 1)))
  (is (false? (p 120)))
  (is (true? (p 119))))
  
(deftest test-solve
  (is (empty? (solve 100)))
  (is (= (solve 200) '[119]))
  (def result '[119 539 959])
  (is (= (solve 1000) result)))
  
(run-tests 'simple-math)
