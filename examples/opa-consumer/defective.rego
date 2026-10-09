package dtfc.authority
import rego.v1
default allow := false
allow if {
    input.action in input.authorized_actions
}
