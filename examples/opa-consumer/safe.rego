package dtfc.authority
import rego.v1
default allow := false
allow if {
    input.authority_state == "active"
    input.action in input.authorized_actions
}
