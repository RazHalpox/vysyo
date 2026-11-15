package com.ultratv.tv.nativeapp.data.tmdb

/** Vysyo : clé TMDB saisie dans les Réglages, recopiée ici au démarrage et à chaque modification. */
object TmdbKey {
    @Volatile var value: String = ""
}
