-- Table: public.cart_items

-- DROP TABLE public.cart_items;

CREATE TABLE IF NOT EXISTS public.cart_items
(
    id bigint NOT NULL DEFAULT nextval('cart_items_id_seq'::regclass),
    scid bigint NOT NULL,
    productid integer,
    quantity integer,
    CONSTRAINT cart_items_pkey PRIMARY KEY (id),
    CONSTRAINT pid FOREIGN KEY (productid)
        REFERENCES public.products (pid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT scid FOREIGN KEY (scid)
        REFERENCES public.shopping_cart (scid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT "quantity must equal or than 0" CHECK (quantity >= 0)
)

TABLESPACE pg_default;

-- Table: public.coupon

-- DROP TABLE public.coupon;

CREATE TABLE IF NOT EXISTS public.coupon
(
    cpid bigint NOT NULL DEFAULT nextval('coupon_cpid_seq'::regclass),
    type text COLLATE pg_catalog."default" NOT NULL,
    code text COLLATE pg_catalog."default" NOT NULL,
    "Activate" boolean NOT NULL DEFAULT true,
    s_time timestamp with time zone,
    e_time timestamp with time zone,
    times integer,
    userids text[] COLLATE pg_catalog."default",
    CONSTRAINT coupon_pkey PRIMARY KEY (cpid)
)

TABLESPACE pg_default;

-- Table: public.customers

-- DROP TABLE public.customers;

CREATE TABLE IF NOT EXISTS public.customers
(
    uid text COLLATE pg_catalog."default" NOT NULL,
    "displayName" text COLLATE pg_catalog."default" NOT NULL,
    language text COLLATE pg_catalog."default",
    "pictureUrl" text COLLATE pg_catalog."default",
    "FirstName" text COLLATE pg_catalog."default",
    "LastName" text COLLATE pg_catalog."default",
    "phoneNumber" text COLLATE pg_catalog."default",
    "Address" text COLLATE pg_catalog."default",
    "Activate" boolean DEFAULT true,
    CONSTRAINT customers_pkey PRIMARY KEY (uid)
)

TABLESPACE pg_default;

-- Table: public.messaging_log

-- DROP TABLE public.messaging_log;

CREATE TABLE IF NOT EXISTS public.messaging_log
(
    id text COLLATE pg_catalog."default" NOT NULL,
    type text COLLATE pg_catalog."default" NOT NULL,
    text text COLLATE pg_catalog."default",
    datetime timestamp with time zone NOT NULL,
    source_uid text COLLATE pg_catalog."default" NOT NULL,
    source_type text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT messaging_log_pkey PRIMARY KEY (id),
    CONSTRAINT source_uid FOREIGN KEY (source_uid)
        REFERENCES public.customers (uid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

-- Table: public.orders

-- DROP TABLE public.orders;

CREATE TABLE IF NOT EXISTS public.orders
(
    oid bigint NOT NULL DEFAULT nextval('orders_oid_seq'::regclass),
    uid text COLLATE pg_catalog."default" NOT NULL,
    scid bigint NOT NULL,
    createddate timestamp with time zone,
    paid bigint,
    ostatus text COLLATE pg_catalog."default" DEFAULT 0,
    CONSTRAINT orders_pkey PRIMARY KEY (oid),
    CONSTRAINT paid FOREIGN KEY (paid)
        REFERENCES public.payment_log (paid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT scid FOREIGN KEY (scid)
        REFERENCES public.shopping_cart (scid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT uid FOREIGN KEY (uid)
        REFERENCES public.customers (uid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

-- Table: public.payment_log

-- DROP TABLE public.payment_log;

CREATE TABLE IF NOT EXISTS public.payment_log
(
    paid bigint NOT NULL DEFAULT nextval('payment_log_paid_seq'::regclass),
    type text COLLATE pg_catalog."default",
    ispaid boolean DEFAULT false,
    paytoken text COLLATE pg_catalog."default",
    tsno text COLLATE pg_catalog."default",
    ts_decp text COLLATE pg_catalog."default",
    ts_status boolean DEFAULT false,
    cardpayurl text COLLATE pg_catalog."default",
    atmpayno text COLLATE pg_catalog."default",
    webatmurl text COLLATE pg_catalog."default",
    opturl text COLLATE pg_catalog."default",
    aptype text COLLATE pg_catalog."default",
    amount integer NOT NULL DEFAULT 0,
    CONSTRAINT payment_log_pkey PRIMARY KEY (paid),
    CONSTRAINT "amount than 0" CHECK (amount >= 0) NOT VALID
)

TABLESPACE pg_default;

-- Table: public.product_category

-- DROP TABLE public.product_category;

CREATE TABLE IF NOT EXISTS public.product_category
(
    pcid integer NOT NULL DEFAULT nextval('product_category_pcid_seq'::regclass),
    category text COLLATE pg_catalog."default" NOT NULL,
    category_decp text COLLATE pg_catalog."default",
    CONSTRAINT product_category_pkey PRIMARY KEY (pcid),
    CONSTRAINT category UNIQUE (category)
)

TABLESPACE pg_default;

-- Table: public.products

-- DROP TABLE public.products;

CREATE TABLE IF NOT EXISTS public.products
(
    pid integer NOT NULL DEFAULT nextval('products_pid_seq'::regclass),
    product_name text COLLATE pg_catalog."default" NOT NULL,
    quantity integer NOT NULL,
    product_decp text COLLATE pg_catalog."default",
    createddate timestamp with time zone,
    expireddate timestamp with time zone,
    price integer NOT NULL DEFAULT 0,
    categoryid integer NOT NULL,
    CONSTRAINT products_pkey PRIMARY KEY (pid),
    CONSTRAINT categoryid FOREIGN KEY (categoryid)
        REFERENCES public.product_category (pcid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT "price must than zero" CHECK (price >= 0)
)

TABLESPACE pg_default;

-- Table: public.shopping_cart

-- DROP TABLE public.shopping_cart;

CREATE TABLE IF NOT EXISTS public.shopping_cart
(
    scid bigint NOT NULL DEFAULT nextval('shopping_cart_scid_seq'::regclass),
    uid text COLLATE pg_catalog."default" NOT NULL,
    createddate timestamp with time zone,
    lock boolean NOT NULL DEFAULT false,
    CONSTRAINT shopping_cart_pkey PRIMARY KEY (scid),
    CONSTRAINT uid FOREIGN KEY (uid)
        REFERENCES public.customers (uid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;