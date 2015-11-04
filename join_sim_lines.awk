/MARC21\/slim$/ {
    getline continuation
    print $0, continuation
}

$0 !~ /MARC21\/slim$/ {
    print
}
