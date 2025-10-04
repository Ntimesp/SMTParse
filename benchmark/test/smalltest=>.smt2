(set-logic QF_NRA)

(declare-const x Real)
(declare-const y Real)

; 如果 x^2 + y^2 <= 1，则 x*y <= 1/2
(assert (=> (<= (+ (* x x) (* y y)) 1) (<= (* x y) 0.5)))

; 如果 x > 0 且 y > 0，则 x^2 + y^2 > 0
(assert (=> (and (> x 0) (> y 0)) (> (+ (* x x) (* y y)) 0)))

(check-sat)
(get-model)