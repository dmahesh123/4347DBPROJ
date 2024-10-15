--
-- PostgreSQL database dump
--

-- Dumped from database version 16.4 (Homebrew)
-- Dumped by pg_dump version 16.4 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: craft; Type: TABLE; Schema: public; Owner: momoqais
--

CREATE TABLE public.craft (
    craftid integer NOT NULL,
    userid integer,
    craftname character varying(100),
    difficultylevel character varying(50),
    estimatedtime integer,
    agerange character varying(50)
);


ALTER TABLE public.craft OWNER TO momoqais;

--
-- Name: craftmaterialrelation; Type: TABLE; Schema: public; Owner: momoqais
--

CREATE TABLE public.craftmaterialrelation (
    craftid integer NOT NULL,
    materialid integer NOT NULL,
    quantityrequired integer
);


ALTER TABLE public.craftmaterialrelation OWNER TO momoqais;

--
-- Name: crafttoolrelation; Type: TABLE; Schema: public; Owner: momoqais
--

CREATE TABLE public.crafttoolrelation (
    craftid integer NOT NULL,
    toolid integer NOT NULL,
    quantityrequired integer
);


ALTER TABLE public.crafttoolrelation OWNER TO momoqais;

--
-- Name: decorativecraft; Type: TABLE; Schema: public; Owner: momoqais
--

CREATE TABLE public.decorativecraft (
    craftid integer NOT NULL
);


ALTER TABLE public.decorativecraft OWNER TO momoqais;

--
-- Name: educationalcraft; Type: TABLE; Schema: public; Owner: momoqais
--

CREATE TABLE public.educationalcraft (
    craftid integer NOT NULL
);


ALTER TABLE public.educationalcraft OWNER TO momoqais;

--
-- Name: instructions; Type: TABLE; Schema: public; Owner: momoqais
--

CREATE TABLE public.instructions (
    instructionid integer NOT NULL,
    craftid integer,
    stepnumber integer,
    description text
);


ALTER TABLE public.instructions OWNER TO momoqais;

--
-- Name: material; Type: TABLE; Schema: public; Owner: momoqais
--

CREATE TABLE public.material (
    materialid integer NOT NULL,
    materialname character varying(100),
    quantity integer,
    price numeric(10,2),
    materialtype character varying(50)
);


ALTER TABLE public.material OWNER TO momoqais;

--
-- Name: recycles; Type: TABLE; Schema: public; Owner: momoqais
--

CREATE TABLE public.recycles (
    materialid integer NOT NULL,
    centerid integer NOT NULL
);


ALTER TABLE public.recycles OWNER TO momoqais;

--
-- Name: recyclingcenter; Type: TABLE; Schema: public; Owner: momoqais
--

CREATE TABLE public.recyclingcenter (
    centerid integer NOT NULL,
    centername character varying(100),
    location character varying(100)
);


ALTER TABLE public.recyclingcenter OWNER TO momoqais;

--
-- Name: seasonalcraft; Type: TABLE; Schema: public; Owner: momoqais
--

CREATE TABLE public.seasonalcraft (
    craftid integer NOT NULL
);


ALTER TABLE public.seasonalcraft OWNER TO momoqais;

--
-- Name: supervises; Type: TABLE; Schema: public; Owner: momoqais
--

CREATE TABLE public.supervises (
    supervisorid integer NOT NULL,
    supervisedid integer NOT NULL
);


ALTER TABLE public.supervises OWNER TO momoqais;

--
-- Name: tool; Type: TABLE; Schema: public; Owner: momoqais
--

CREATE TABLE public.tool (
    toolid integer NOT NULL,
    toolname character varying(100),
    price numeric(10,2),
    tooltype character varying(50)
);


ALTER TABLE public.tool OWNER TO momoqais;

--
-- Name: users; Type: TABLE; Schema: public; Owner: momoqais
--

CREATE TABLE public.users (
    userid integer NOT NULL,
    usertype character varying(50),
    username character varying(100),
    email character varying(100)
);


ALTER TABLE public.users OWNER TO momoqais;

--
-- Data for Name: craft; Type: TABLE DATA; Schema: public; Owner: momoqais
--

COPY public.craft (craftid, userid, craftname, difficultylevel, estimatedtime, agerange) FROM stdin;
1	1	Paper Airplane	Easy	15	5-10
2	2	Origami Crane	Medium	30	10-15
4	4	Wooden Birdhouse	Hard	90	12-18
5	5	Clay Sculpture	Medium	60	10-16
6	6	Knitted Scarf	Hard	120	12-18
7	7	Paper Mache Mask	Medium	45	10-15
8	8	DIY Picture Frame	Easy	30	8-12
9	9	Christmas Ornament	Easy	20	5-10
10	10	Lego Robot	Medium	60	10-15
3	3	Beaded Bracelet	Very Hard	20	8-12
\.


--
-- Data for Name: craftmaterialrelation; Type: TABLE DATA; Schema: public; Owner: momoqais
--

COPY public.craftmaterialrelation (craftid, materialid, quantityrequired) FROM stdin;
1	1	1
2	1	1
3	2	20
4	3	5
5	4	1
6	5	2
7	1	3
8	10	2
9	6	1
10	8	50
\.


--
-- Data for Name: crafttoolrelation; Type: TABLE DATA; Schema: public; Owner: momoqais
--

COPY public.crafttoolrelation (craftid, toolid, quantityrequired) FROM stdin;
1	1	1
2	2	1
3	3	1
4	4	1
5	2	1
6	3	1
7	6	1
8	1	1
9	2	1
10	9	1
\.


--
-- Data for Name: decorativecraft; Type: TABLE DATA; Schema: public; Owner: momoqais
--

COPY public.decorativecraft (craftid) FROM stdin;
3
6
8
\.


--
-- Data for Name: educationalcraft; Type: TABLE DATA; Schema: public; Owner: momoqais
--

COPY public.educationalcraft (craftid) FROM stdin;
2
5
10
\.


--
-- Data for Name: instructions; Type: TABLE DATA; Schema: public; Owner: momoqais
--

COPY public.instructions (instructionid, craftid, stepnumber, description) FROM stdin;
1	1	1	Fold the paper in half lengthwise.
2	1	2	Fold the corners into triangles.
3	1	3	Fold the wings down.
4	2	1	Fold the paper into a square.
5	2	2	Fold diagonally to form a triangle.
6	2	3	Bring the edges together to form a crane shape.
7	3	1	Thread the beads onto the string.
8	3	2	Tie a knot at the end of the string.
9	4	1	Cut the wooden pieces according to the measurements.
10	4	2	Assemble the pieces to form the birdhouse.
\.


--
-- Data for Name: material; Type: TABLE DATA; Schema: public; Owner: momoqais
--

COPY public.material (materialid, materialname, quantity, price, materialtype) FROM stdin;
1	Paper	100	0.10	Paper
2	Beads	200	0.05	Plastic
3	Wood	50	1.50	Wood
4	Clay	30	2.00	Plastic
5	Yarn	40	1.20	Fabric
6	Paint	25	3.00	Glass
7	Glue	50	0.50	Plastic
8	Lego Bricks	500	0.15	Plastic
9	Wire	100	0.75	Metal
10	Fabric	60	1.00	Fabric
11	Cardboard	50	0.75	Paper
\.


--
-- Data for Name: recycles; Type: TABLE DATA; Schema: public; Owner: momoqais
--

COPY public.recycles (materialid, centerid) FROM stdin;
1	1
2	2
3	3
4	4
5	5
6	6
7	7
8	8
9	9
10	10
\.


--
-- Data for Name: recyclingcenter; Type: TABLE DATA; Schema: public; Owner: momoqais
--

COPY public.recyclingcenter (centerid, centername, location) FROM stdin;
1	City Recycling Center	Downtown
2	Green Earth Recycling	Suburbs
3	Eco Friendly Recycling	Uptown
4	Neighborhood Recycling	Residential Area
5	Community Recycling	Park Area
6	Reclaim and Recycle	Industrial Zone
7	Planet Care Recycling	City Outskirts
8	GreenCycle	Main Street
9	Future Earth Recycling	Town Center
10	Clean Earth Recycling	Rural Area
\.


--
-- Data for Name: seasonalcraft; Type: TABLE DATA; Schema: public; Owner: momoqais
--

COPY public.seasonalcraft (craftid) FROM stdin;
1
4
9
\.


--
-- Data for Name: supervises; Type: TABLE DATA; Schema: public; Owner: momoqais
--

COPY public.supervises (supervisorid, supervisedid) FROM stdin;
1	2
3	5
4	6
1	8
7	10
1	9
6	8
9	10
4	7
3	4
\.


--
-- Data for Name: tool; Type: TABLE DATA; Schema: public; Owner: momoqais
--

COPY public.tool (toolid, toolname, price, tooltype) FROM stdin;
1	Scissors	2.00	Cutting
2	Paintbrush	1.50	Painting
3	Needle	1.00	Sewing
4	Hammer	5.00	Building
6	Hot Glue Gun	7.00	Adhesive
7	Saw	8.00	Cutting
8	Pliers	4.50	Bending
9	Lego Separator	2.00	Building
10	Measuring Tape	1.75	Measuring
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: momoqais
--

COPY public.users (userid, usertype, username, email) FROM stdin;
1	Teacher	Alice Johnson	alice.johnson@example.com
2	Student	Bob Smith	bob.smith@example.com
3	Parent	Carol White	carol.white@example.com
4	Teacher	David Green	david.green@example.com
5	Student	Eve Brown	eve.brown@example.com
6	Teacher	Frank Thomas	frank.thomas@example.com
7	Parent	Grace Kelly	grace.kelly@example.com
8	Student	Henry Adams	henry.adams@example.com
9	Teacher	Ivy Martin	ivy.martin@example.com
10	Student	Jake Turner	jake.turner@example.com
\.


--
-- Name: craft craft_pkey; Type: CONSTRAINT; Schema: public; Owner: momoqais
--

ALTER TABLE ONLY public.craft
    ADD CONSTRAINT craft_pkey PRIMARY KEY (craftid);


--
-- Name: craftmaterialrelation craftmaterialrelation_pkey; Type: CONSTRAINT; Schema: public; Owner: momoqais
--

ALTER TABLE ONLY public.craftmaterialrelation
    ADD CONSTRAINT craftmaterialrelation_pkey PRIMARY KEY (craftid, materialid);


--
-- Name: crafttoolrelation crafttoolrelation_pkey; Type: CONSTRAINT; Schema: public; Owner: momoqais
--

ALTER TABLE ONLY public.crafttoolrelation
    ADD CONSTRAINT crafttoolrelation_pkey PRIMARY KEY (craftid, toolid);


--
-- Name: decorativecraft decorativecraft_pkey; Type: CONSTRAINT; Schema: public; Owner: momoqais
--

ALTER TABLE ONLY public.decorativecraft
    ADD CONSTRAINT decorativecraft_pkey PRIMARY KEY (craftid);


--
-- Name: educationalcraft educationalcraft_pkey; Type: CONSTRAINT; Schema: public; Owner: momoqais
--

ALTER TABLE ONLY public.educationalcraft
    ADD CONSTRAINT educationalcraft_pkey PRIMARY KEY (craftid);


--
-- Name: instructions instructions_pkey; Type: CONSTRAINT; Schema: public; Owner: momoqais
--

ALTER TABLE ONLY public.instructions
    ADD CONSTRAINT instructions_pkey PRIMARY KEY (instructionid);


--
-- Name: material material_pkey; Type: CONSTRAINT; Schema: public; Owner: momoqais
--

ALTER TABLE ONLY public.material
    ADD CONSTRAINT material_pkey PRIMARY KEY (materialid);


--
-- Name: recycles recycles_pkey; Type: CONSTRAINT; Schema: public; Owner: momoqais
--

ALTER TABLE ONLY public.recycles
    ADD CONSTRAINT recycles_pkey PRIMARY KEY (materialid, centerid);


--
-- Name: recyclingcenter recyclingcenter_pkey; Type: CONSTRAINT; Schema: public; Owner: momoqais
--

ALTER TABLE ONLY public.recyclingcenter
    ADD CONSTRAINT recyclingcenter_pkey PRIMARY KEY (centerid);


--
-- Name: seasonalcraft seasonalcraft_pkey; Type: CONSTRAINT; Schema: public; Owner: momoqais
--

ALTER TABLE ONLY public.seasonalcraft
    ADD CONSTRAINT seasonalcraft_pkey PRIMARY KEY (craftid);


--
-- Name: supervises supervises_pkey; Type: CONSTRAINT; Schema: public; Owner: momoqais
--

ALTER TABLE ONLY public.supervises
    ADD CONSTRAINT supervises_pkey PRIMARY KEY (supervisorid, supervisedid);


--
-- Name: tool tool_pkey; Type: CONSTRAINT; Schema: public; Owner: momoqais
--

ALTER TABLE ONLY public.tool
    ADD CONSTRAINT tool_pkey PRIMARY KEY (toolid);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: momoqais
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (userid);


--
-- Name: craft craft_userid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: momoqais
--

ALTER TABLE ONLY public.craft
    ADD CONSTRAINT craft_userid_fkey FOREIGN KEY (userid) REFERENCES public.users(userid);


--
-- Name: craftmaterialrelation craftmaterialrelation_craftid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: momoqais
--

ALTER TABLE ONLY public.craftmaterialrelation
    ADD CONSTRAINT craftmaterialrelation_craftid_fkey FOREIGN KEY (craftid) REFERENCES public.craft(craftid);


--
-- Name: craftmaterialrelation craftmaterialrelation_materialid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: momoqais
--

ALTER TABLE ONLY public.craftmaterialrelation
    ADD CONSTRAINT craftmaterialrelation_materialid_fkey FOREIGN KEY (materialid) REFERENCES public.material(materialid);


--
-- Name: crafttoolrelation crafttoolrelation_craftid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: momoqais
--

ALTER TABLE ONLY public.crafttoolrelation
    ADD CONSTRAINT crafttoolrelation_craftid_fkey FOREIGN KEY (craftid) REFERENCES public.craft(craftid);


--
-- Name: crafttoolrelation crafttoolrelation_toolid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: momoqais
--

ALTER TABLE ONLY public.crafttoolrelation
    ADD CONSTRAINT crafttoolrelation_toolid_fkey FOREIGN KEY (toolid) REFERENCES public.tool(toolid);


--
-- Name: decorativecraft decorativecraft_craftid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: momoqais
--

ALTER TABLE ONLY public.decorativecraft
    ADD CONSTRAINT decorativecraft_craftid_fkey FOREIGN KEY (craftid) REFERENCES public.craft(craftid);


--
-- Name: educationalcraft educationalcraft_craftid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: momoqais
--

ALTER TABLE ONLY public.educationalcraft
    ADD CONSTRAINT educationalcraft_craftid_fkey FOREIGN KEY (craftid) REFERENCES public.craft(craftid);


--
-- Name: instructions instructions_craftid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: momoqais
--

ALTER TABLE ONLY public.instructions
    ADD CONSTRAINT instructions_craftid_fkey FOREIGN KEY (craftid) REFERENCES public.craft(craftid);


--
-- Name: recycles recycles_centerid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: momoqais
--

ALTER TABLE ONLY public.recycles
    ADD CONSTRAINT recycles_centerid_fkey FOREIGN KEY (centerid) REFERENCES public.recyclingcenter(centerid);


--
-- Name: recycles recycles_materialid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: momoqais
--

ALTER TABLE ONLY public.recycles
    ADD CONSTRAINT recycles_materialid_fkey FOREIGN KEY (materialid) REFERENCES public.material(materialid);


--
-- Name: seasonalcraft seasonalcraft_craftid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: momoqais
--

ALTER TABLE ONLY public.seasonalcraft
    ADD CONSTRAINT seasonalcraft_craftid_fkey FOREIGN KEY (craftid) REFERENCES public.craft(craftid);


--
-- Name: supervises supervises_supervisedid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: momoqais
--

ALTER TABLE ONLY public.supervises
    ADD CONSTRAINT supervises_supervisedid_fkey FOREIGN KEY (supervisedid) REFERENCES public.users(userid);


--
-- Name: supervises supervises_supervisorid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: momoqais
--

ALTER TABLE ONLY public.supervises
    ADD CONSTRAINT supervises_supervisorid_fkey FOREIGN KEY (supervisorid) REFERENCES public.users(userid);


--
-- PostgreSQL database dump complete
--

