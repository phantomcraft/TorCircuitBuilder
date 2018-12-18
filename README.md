# Tor Circuit Builder

Get as many Tor IPs as you could ever want. Legally for things like _metrics_,
and other things like that! What other uses could someone have for needing a
ton of concurrent Tor IPs anyway?

## Requirements

Debian/Ubuntu package `python-stem`. This is Tor's control library.

## Usage

There's literally no configuration options - if you can't figure out how to use
this based on the directions, you honestly don't even deserve to use it.

The number of IPs is set on `tor-circuit-builder.py` lines *34*, *35*, and *39*.

## Caveats

Creating circuits is expensive on the Tor network. Not that you'd care, you
insensitive fuck.

Once you run Tor Circuit Builder, if you stop it, new Tor connections will no
longer work until you restart tor. This is because Tor Circuit Builder sets
the `__LeaveStreamsUnattached` configuration option.

Each time you connect to Tor SOCKS5 port (usually 9050), the connection will
be handed off _to a random circuit_. That means that if you are relying on
any cookies, ensure that the server doesn't mandate that IPs remain the same
across sessions. Otherwise, you will need to set the HTTP client to use
Keepalive. If you don't know what that means, if you're trying to bot a website
that uses PHP it will probably break.

## Donations

lmao bet. i make more money than you fucker

## Shoutout to my knee grow @/lumlnous

Enjoy, jajaja