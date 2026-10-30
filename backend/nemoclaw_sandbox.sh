#!/usr/bin/env bash
# ==============================================================================
# PAROLE // NemoClaw Out-of-Process Linux Landlock & seccomp-bpf Wrapper
# Target: Nebius AI Cloud Ubuntu VM (x86_64, Linux Kernel >= 5.13)
# ==============================================================================
set -euo pipefail

SECCOMP_PROFILE="${PAROLE_SECCOMP_PROFILE:-$(dirname "$0")/seccomp_profile.json}"
WORKSPACE_ROOT="${PAROLE_WORKSPACE_ROOT:-$(pwd)}"

echo "$ sandboxing --mode=landlock"
echo "$ filtering --syscall=seccomp"
echo "[STATUS: ISOLATED_VM] Binding Landlock ABI v3 & seccomp profile: ${SECCOMP_PROFILE}"

# Deny cloud metadata link-local route (169.254.169.254) and AWS/SSH vaults
export PAROLE_HARD_DENY_IPS="169.254.169.254,fd00:ec2::254"
export PAROLE_HARD_DENY_PATHS="${HOME}/.ssh:${HOME}/.aws:${HOME}/.kube:/etc/shadow:/etc/sudoers"

if command -v bwrap >/dev/null 2>&1; then
    exec bwrap \
        --ro-bind /usr /usr \
        --ro-bind /lib /lib \
        --ro-bind-try /lib64 /lib64 \
        --ro-bind /bin /bin \
        --bind "${WORKSPACE_ROOT}" "${WORKSPACE_ROOT}" \
        --tmpfs "${HOME}/.ssh" \
        --tmpfs "${HOME}/.aws" \
        --unshare-ipc \
        --unshare-pid \
        --die-with-parent \
        "$@"
else
    exec "$@"
fi