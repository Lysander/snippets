#lang scheme
;;;; simple crypt-algo corresponding to a thread:
;;;;    http://www.python-forum.de/viewtopic.php?f=11&t=25313

;;; converts a list of chars into a list of bytes and vice versa
;;; as method chose "integer->char" or "char->integer"
(define (map method data)
    (if (null? data) 
        '()
        (cons (method (car data)) (map method (cdr data)))))

(define (bytes->chars bytes)
    (map integer->char bytes))

(define (chars->bytes chars)
    (map char->integer chars))    

;;; core crypto function, walk through a list of bytes, increments a counter
;;; and adds or substract its value to the corresponding byte.
(define (_crypt bytes counter op)
    (if (null? bytes)
        '()
        (cons (op (car bytes) counter) (_crypt (cdr bytes) (+ 1 counter) op))))

;;; klappt so noch net
(define (reduce op bytes)
    (if (null? bytes)
        (cons 0 '())
        (let ((res (reduce op (cdr bytes))))
        (cons (op (car bytes) (+ 1 (car res))) (cdr res)))))

;;; wrapper function for _crypt, converts a given string into a list of bytes
;;; before calling the _crypt function and vice versa after to return a string
(define (crypt text op)
    (list->string (bytes->chars (reduce op (chars->bytes (string->list text))))))

(define (encrypt text)
    (crypt text +))

(define (decrypt text)
    (crypt text -))
    
(encrypt "Python")
(decrypt "Pzvkss")