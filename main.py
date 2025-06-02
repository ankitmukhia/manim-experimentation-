from manim import *

# This Manim script generates a SINGLE MP4 video file demonstrating the
# client, server, and caching workflow step-by-step.

class ClientServerCacheScene(Scene):
    def construct(self):
        # 0. Configuration
        client_pos = LEFT * 4.5
        server_pos = RIGHT * 4.5
        cache_pos = ORIGIN + DOWN * 0.2

        box_height = 1.5
        box_width = 2.8

        def create_labeled_box(label_text, position, color):
            box = Rectangle(width=box_width, height=box_height, color=color, fill_opacity=0.25)
            box.set_stroke(width=2)
            label = Text(label_text, font_size=28, weight=BOLD).move_to(box.get_center())
            group = VGroup(box, label).move_to(position)
            return group

        client = create_labeled_box("Client", client_pos, BLUE_C)
        server = create_labeled_box("Server", server_pos, GREEN_C)
        cache = create_labeled_box("Cache", cache_pos, YELLOW_C)

        server_data_store_label = Text("DB", font_size=18, color=WHITE).next_to(server, DOWN, buff=0.1)
        cache_memory_label = Text("Mem", font_size=18, color=WHITE).next_to(cache, DOWN, buff=0.1)

        data_v1_text = "Data v1"
        server_data_obj = Text(data_v1_text, font_size=22, color=WHITE).move_to(server.get_center() + UP * 0.1)

        self.play(
            FadeIn(client, shift=LEFT*0.5),
            FadeIn(server, shift=RIGHT*0.5),
            FadeIn(cache, shift=DOWN*0.5),
            Write(server_data_obj),
            Write(server_data_store_label),
            Write(cache_memory_label)
        )
        self.wait(1)

        status_text = Text("1. Initial Request (Cache Miss)", font_size=30, color=WHITE).to_edge(UP, buff=0.5)
        self.play(Write(status_text))

        req_c_s_arrow = Arrow(client.get_right(), server.get_left(), buff=0.2, color=PINK, stroke_width=5, max_tip_length_to_length_ratio=0.2)
        req_c_s_label = Text("GET /data", font_size=20).next_to(req_c_s_arrow, UP, buff=0.1)
        self.play(GrowArrow(req_c_s_arrow), Write(req_c_s_label))
        self.wait(0.7)

        self.play(Indicate(server_data_obj, color=GREEN_A, scale_factor=1.1))
        self.wait(0.5)

        # ***** MODIFIED LINE *****
        res_s_c_arrow = Arrow(server.get_left(), client.get_right(), buff=0.2, color=BLUE_B, stroke_width=5, max_tip_length_to_length_ratio=0.2)
        res_s_c_label = Text(data_v1_text, font_size=20).next_to(res_s_c_arrow, UP, buff=0.1)
        self.play(GrowArrow(res_s_c_arrow), Write(res_s_c_label))
        self.wait(0.7)

        store_s_cache_arrow = Arrow(server.get_edge_center(DOWN) + LEFT*0.3, cache.get_edge_center(UP) + RIGHT*0.3, buff=0.2, color=ORANGE, stroke_width=5, max_tip_length_to_length_ratio=0.2)
        store_s_cache_label = Text(f"Store: {data_v1_text}", font_size=20).next_to(store_s_cache_arrow, RIGHT, buff=0.1)
        cached_data_obj_v1 = server_data_obj.copy().move_to(cache.get_center() + UP * 0.1)
        self.play(
            GrowArrow(store_s_cache_arrow),
            Write(store_s_cache_label),
            FadeIn(cached_data_obj_v1, shift=UP*0.2)
        )
        self.wait(1.2)

        self.play(
            FadeOut(req_c_s_arrow), FadeOut(req_c_s_label),
            FadeOut(res_s_c_arrow), FadeOut(res_s_c_label),
            FadeOut(store_s_cache_arrow), FadeOut(store_s_cache_label)
        )
        self.play(FadeOut(status_text, shift=UP*0.2))
        self.wait(0.5)

        status_text = Text("2. Cached Request (Cache Hit)", font_size=30, color=WHITE).to_edge(UP, buff=0.5)
        self.play(Write(status_text))

        req_c_cache_arrow = Arrow(client.get_right(), cache.get_left(), buff=0.2, color=PINK, stroke_width=5, max_tip_length_to_length_ratio=0.2)
        req_c_cache_label = Text("GET /data", font_size=20).next_to(req_c_cache_arrow, UP, buff=0.1)
        self.play(GrowArrow(req_c_cache_arrow), Write(req_c_cache_label))
        self.wait(0.7)

        # ***** MODIFIED LINE *****
        res_cache_c_arrow = Arrow(cache.get_left(), client.get_right(), buff=0.2, color=BLUE_B, stroke_width=5, max_tip_length_to_length_ratio=0.2)
        res_cache_c_label = Text(f"{data_v1_text} (from Cache)", font_size=20).next_to(res_cache_c_arrow, UP, buff=0.1)
        self.play(
            GrowArrow(res_cache_c_arrow),
            Write(res_cache_c_label),
            Indicate(cached_data_obj_v1, color=YELLOW_A, scale_factor=1.2)
        )
        self.wait(1.2)

        self.play(
            FadeOut(req_c_cache_arrow), FadeOut(req_c_cache_label),
            FadeOut(res_cache_c_arrow), FadeOut(res_cache_c_label)
        )
        self.play(FadeOut(status_text, shift=UP*0.2))
        self.wait(0.5)

        status_text = Text("3. Data Update on Server", font_size=30, color=WHITE).to_edge(UP, buff=0.5)
        self.play(Write(status_text))

        data_v2_text = "Data v2"
        new_server_data_obj = Text(data_v2_text, font_size=22, color=WHITE).move_to(server_data_obj.get_center())
        update_flash = Flash(server, color=RED_C, flash_radius=box_width*1.1, line_length=0.3, num_lines=12, run_time=1)
        server_update_label = Text("Data Updated!", font_size=22, color=RED_C).next_to(server, UP, buff=0.25)
        self.play(
            Transform(server_data_obj, new_server_data_obj),
            Write(server_update_label),
            update_flash
        )
        self.wait(1.2)
        self.play(FadeOut(server_update_label))
        self.play(FadeOut(status_text, shift=UP*0.2))
        self.wait(0.5)

        status_text = Text("4. Request Updated Data (Stale Cache)", font_size=30, color=WHITE).to_edge(UP, buff=0.5)
        self.play(Write(status_text))

        req_c_cache_arrow_2 = Arrow(client.get_right(), cache.get_left(), buff=0.2, color=PINK, stroke_width=5, max_tip_length_to_length_ratio=0.2)
        req_c_cache_label_2 = Text("GET /data", font_size=20).next_to(req_c_cache_arrow_2, UP, buff=0.1)
        self.play(GrowArrow(req_c_cache_arrow_2), Write(req_c_cache_label_2))
        self.wait(0.7)

        stale_label = Text("(Stale: v1)", font_size=18, color=RED_B).next_to(cached_data_obj_v1, DOWN, buff=0.15)
        self.play(Write(stale_label), Indicate(cached_data_obj_v1, color=RED_B, scale_factor=1.2))
        self.wait(1)

        req_cache_s_arrow = Arrow(cache.get_right(), server.get_left(), buff=0.2, color=ORANGE, stroke_width=5, max_tip_length_to_length_ratio=0.2)
        req_cache_s_label = Text("GET /data (check)", font_size=18).next_to(req_cache_s_arrow, UP, buff=0.1)
        self.play(GrowArrow(req_cache_s_arrow), Write(req_cache_s_label))
        self.wait(0.7)

        res_s_cache_arrow = Arrow(server.get_left(), cache.get_right(), buff=0.2, color=GREEN_A, stroke_width=5, max_tip_length_to_length_ratio=0.2)
        res_s_cache_label = Text(f"Fresh: {data_v2_text}", font_size=20).next_to(res_s_cache_arrow, UP, buff=0.1)
        new_cached_data_obj = Text(data_v2_text, font_size=22, color=WHITE).move_to(cached_data_obj_v1.get_center())
        self.play(
            GrowArrow(res_s_cache_arrow),
            Write(res_s_cache_label),
            Indicate(server_data_obj, color=GREEN_A)
        )
        self.wait(0.7)

        cache_update_flash = Flash(cache, color=YELLOW_A, flash_radius=box_width*1.1, line_length=0.3, num_lines=12, run_time=1)
        self.play(
            Transform(cached_data_obj_v1, new_cached_data_obj),
            FadeOut(stale_label, shift=DOWN*0.2),
            cache_update_flash
        )
        self.wait(0.7)

        # ***** MODIFIED LINE *****
        res_cache_c_arrow_2 = Arrow(cache.get_left(), client.get_right(), buff=0.2, color=BLUE_B, stroke_width=5, max_tip_length_to_length_ratio=0.2)
        res_cache_c_label_2 = Text(f"{data_v2_text} (Fresh from Cache)", font_size=20).next_to(res_cache_c_arrow_2, UP, buff=0.1)
        self.play(
            GrowArrow(res_cache_c_arrow_2),
            Write(res_cache_c_label_2),
            Indicate(cached_data_obj_v1, color=YELLOW_A, scale_factor=1.2)
        )
        self.wait(1.5)

        self.play(
            FadeOut(req_c_cache_arrow_2), FadeOut(req_c_cache_label_2),
            FadeOut(req_cache_s_arrow), FadeOut(req_cache_s_label),
            FadeOut(res_s_cache_arrow), FadeOut(res_s_cache_label),
            FadeOut(res_cache_c_arrow_2), FadeOut(res_cache_c_label_2)
        )
        self.play(FadeOut(status_text, shift=UP*0.2))
        self.wait(1)

        final_text = Text("Workflow Complete!", font_size=40, weight=BOLD).to_edge(UP, buff=0.5)
        self.play(Write(final_text))
        self.wait(3)
        self.play(
            LaggedStart(
                FadeOut(client, shift=LEFT*0.5),
                FadeOut(server, shift=RIGHT*0.5),
                FadeOut(cache, shift=UP*0.5),
                FadeOut(server_data_obj),
                FadeOut(cached_data_obj_v1),
                FadeOut(server_data_store_label),
                FadeOut(cache_memory_label),
                FadeOut(final_text, shift=UP*0.2),
                lag_ratio=0.15
            )
        )
        self.wait(1)
