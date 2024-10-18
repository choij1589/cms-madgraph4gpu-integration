#!/bin/bash
draw_backend_comparison() {
    local process=$1
    BackendComparison.py --process $process
}

draw_jetbinned_comparison() {
    local process=$1
    local backend=$2
    JetBinnedComparison.py --process $process --backend $backend
}

processes=(
    "DY0j" "DY1j" "DY2j" "DY3j" "DY4j-Simplified" "DY01234j-Simplified"
    "TT0j" "TT1j" "TT2j" "TT3j" "TT0123j"
)
export -f draw_backend_comparison
parallel draw_backend_comparison ::: "${processes[@]}"

processes=("DY" "TT")
backends=("FORTRAN" "CPP" "CUDA")
export -f draw_jetbinned_comparison
parallel draw_jetbinned_comparison ::: "${processes[@]}" ::: "${backends[@]}"
