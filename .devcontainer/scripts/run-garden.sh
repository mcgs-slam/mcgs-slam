#!/usr/bin/env bash
set -euo pipefail

mode="${1:-smoke}"
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_dir="$(cd "${script_dir}/../.." && pwd)"
dataset="${MCGS_GARDEN:-/datasets/garden}"

cd "${repo_dir}"
python .devcontainer/scripts/validate_garden.py

image_dirs=(
    "${dataset}/images/front_left"
    "${dataset}/images/front_center"
    "${dataset}/images/front_right"
    "${dataset}/images/left_center"
    "${dataset}/images/right_center"
)

common_args=(
    --calib calib/drones.yml
    --imagedir "${image_dirs[@]}"
)

case "${mode}" in
    smoke)
        exec python demo.py "${common_args[@]}" \
            --stride 3 \
            --early_stop 12 \
            --output output/garden-smoke
        ;;
    full)
        exec python demo.py "${common_args[@]}" \
            --stride 1 \
            --output output/garden
        ;;
    *)
        echo "Usage: $0 [smoke|full]" >&2
        exit 2
        ;;
esac
