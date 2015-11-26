;;
;; Solutions for the exercise within this discussion thread:
;; https://forum.ubuntuusers.de/topic/algorithmus-bilden
;;
;; First block is the attempt to translate the C solution directly to clojure:
;; https://forum.ubuntuusers.de/topic/algorithmus-bilden/2/#post-7911593
;; It lacks TCO-Possibilities, therefor the better second solution exist.
;;
(ns snippets.squared)

(defn mul [a b]
  "Simple recursive multiplication function. It lacks TC and should not be 
  used in production."
  (cond
    (zero? b)
      0
    (= b 1) 
      a
    :else
    (+ a (mul a (- b 1)))))
    
(defn pow [b e]
  "Simple recursive power function. It powers the base b with the exponent e.
  It also lacks TC and should not be used in production"
  (cond
    (zero? e)
      1
    (= e 1)
      b
    :else
      (mul b (pow b (- e 1)))))
    
(defn squared [x]
  "Calculates the square of a given value x"
  (pow x 2))


;;
;; And now the "better" implementation with TCO potential by adding an 
;; accumulator. So the "work" of addition is done with each recursion step 
;; downwards, so that the recursive call is in the ending. 
;;
;; That is a quite usefull pattern within functional programming!
;;

(defn tc-mul [a b]
  "Muliplies two values a and b by recursively summing up the first value.
  It uses a internal function with a 3rd accumulator parameter in order
  to have a recursive tail call"
  (letfn [(mul-acc [a b acc]
            (if (zero? b)
              acc
              (recur a (dec b) (+ acc a))))]
    (cond
        (zero? b)
          0
        (= b 1)
          a
        :else
          (mul-acc a b 0))))
    
(defn tc-pow [b e]
  "This recursive power function, powers the base b with the exponent e.
  It uses an internal helper function with an accumulator as 3rd parameter
  in order to have a real tail call."
  (letfn [(pow-acc [b e acc]
            (if (zero? e)
              acc
            (recur b (dec e) (tc-mul acc b))))]
    (cond
      (zero? e) 
        1
      (= e 1)
        b
      :else
        (pow-acc b e 1))))

(defn tc-squared [x]
  "Calculates the square of a given value x with TC functions."
  (tc-pow x 2))
