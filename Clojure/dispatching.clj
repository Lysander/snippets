;
; Simple Dispatching in Clojure
;

(defn foo []
  (println "Foo has been called"))

(defn bar []
  (println "Bar has been called"))
  
(def dispatcher {:f foo :b bar})

(defn get-user-choice []
  (keyword (read-line)))
  
(defn dispatch-by-choice [choice]
  ((choice dispatcher)))
  
(dispatch-by-choice (get-user-choice))