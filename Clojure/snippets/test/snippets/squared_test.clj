(ns snippets.squared-test
  (:require [clojure.test :refer :all]
            [snippets.squared :refer :all]))

(deftest test-mul
  (is (zero? (mul 1 0)))
  (is (= 2 (mul 2 1)))
  (is (= 12 (mul 3 4))))

(deftest test-pow
  (is (= 1 (pow 1 0)))
  (is (= 2 (pow 2 1)))
  (is (= 8 (pow 2 3)))
  (is (= 144 (pow 12 2))))

(deftest test-squared
  (is (= 0 (squared 0)))
  (is (= 1 (squared 1)))
  (is (= 4 (squared 2)))
  (is (= 9 (squared 3)))
  (is (= 16 (squared 4)))
  (is (= 144 (squared 12))))

(deftest test-tc-mul
  (is (zero? (tc-mul 1 0)))
  (is (= 2 (tc-mul 2 1)))
  (is (= 12 (tc-mul 3 4))))

(deftest test-tc-pow
  (is (= 1 (tc-pow 1 0)))
  (is (= 2 (tc-pow 2 1)))
  (is (= 8 (tc-pow 2 3)))
  (is (= 144 (tc-pow 12 2))))

(deftest test-tc-squared
  (is (= 0 (tc-squared 0)))
  (is (= 1 (tc-squared 1)))
  (is (= 4 (tc-squared 2)))
  (is (= 9 (tc-squared 3)))
  (is (= 16 (tc-squared 4)))
  (is (= 144 (tc-squared 12))))
