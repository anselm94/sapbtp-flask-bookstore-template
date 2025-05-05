using {
    Currency,
    managed,
} from '@sap/cds/common';

namespace sap.sample.bookshop;

entity Books : managed {
    key ID       : Integer;
        title    : String(111)            @mandatory;
        descr    : String(1111);
        stock    : Integer;
        price    : Price;
        currency : Currency;
        author   : Association to Authors @mandatory;
        genre    : Association to Genres;
}

entity Authors : managed {
    key ID           : Integer;
        name         : String(111) @mandatory;
        dateOfBirth  : Date;
        dateOfDeath  : Date;
        placeOfBirth : String;
        placeOfDeath : String;
        books        : Association to many Books
                           on books.author = $self;
}

/** Hierarchically organized Code List for Genres */
entity Genres {
    key ID       : UUID;
        name     : String(255);
        descr    : String(1000);
        parent   : Association to Genres;
        children : Composition of many Genres
                       on children.parent = $self;
}

type Price : Decimal(9, 2);
