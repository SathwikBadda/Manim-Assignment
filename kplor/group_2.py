from manim import *
# from manim_physics import *
import numpy as np

class FinalScene(MovingCameraScene):
    def construct(self):
        # Section 1
        bg_color = "#5B4BDB"
        bg = Rectangle(width=16, height=9, fill_color=bg_color, fill_opacity=1, stroke_width=0)
        bg.move_to(ORIGIN)
        bg.set_z_index(0)
        self.add(bg)
        
        grid_nodes = []
        node_positions = []
        for x in np.linspace(-7, 7, 15):
            for y in np.linspace(-7, 7, 15):
                node_positions.append(np.array([x, y, 0]))
        
        node_anims = []
        for pos in node_positions:
            node = Circle(radius=0.15, fill_color="#2DD4BF", fill_opacity=1, stroke_width=0)
            node.move_to(pos)
            node.scale(0)
            node.set_z_index(2)
            grid_nodes.append(node)
            self.add(node)
        
        for i, (node, pos) in enumerate(zip(grid_nodes, node_positions)):
            direction = pos / (np.linalg.norm(pos) + 0.1)
            node_anims.append(GrowFromEdge(node, direction))
        
        self.play(LaggedStart(*node_anims, lag_ratio=0.02), run_time=2.1)
        
        connection_lines = []
        for i, pos_i in enumerate(node_positions):
            for j, pos_j in enumerate(node_positions):
                if i < j and np.linalg.norm(pos_i - pos_j) < 1.5:
                    line = Line(pos_i, pos_j, color="#FF6B9A", stroke_width=1)
                    line.set_z_index(1)
                    connection_lines.append(line)
                    self.add(line)
        
        line_anims = [Create(line) for line in connection_lines]
        self.play(LaggedStart(*line_anims, lag_ratio=0.01), run_time=2.1)
        
        pulse_updaters = []
        for node in grid_nodes:
            def make_pulse(n, t_offset):
                def updater(m, dt):
                    scale_val = 0.15 * (0.14 + 0.02 * (0.5 + 0.5 * np.sin(2 * np.pi * (self.renderer.time + t_offset) * 0.5)))
                    m.set_width(2 * scale_val)
                return updater
            pulse_updaters.append(make_pulse(node, np.random.rand()))
            node.add_updater(pulse_updaters[-1])
        
        particles = []
        for _ in range(30):
            particle = Circle(radius=0.08, fill_color="#2DD4BF", fill_opacity=0.6, stroke_width=0)
            particle.move_to(np.array([np.random.uniform(-8, 8), np.random.uniform(-8, 8), 0]))
            particle.set_z_index(1)
            particles.append(particle)
            self.add(particle)
        
        def particle_updater(particles_list, dt):
            for p in particles_list:
                p.shift(np.array([0.3 * dt, 0, 0]))
                if p.get_x() > 8:
                    p.set_x(-8)
                closest_dist = min([np.linalg.norm(p.get_center() - node.get_center()) for node in grid_nodes])
                if closest_dist < 1.5:
                    p.set_fill_opacity(min(1.2, 0.6 + (1.5 - closest_dist) * 0.4))
                else:
                    p.set_fill_opacity(0.6)
        
        self.add_updater(lambda dt: particle_updater(particles, dt))
        
        self.wait(3.2)
        
        self.wait(3.26)
        
        # Section 2
        price_text = Text("₹500", font="Girder 117", font_size=48, color="#F8FAFC")
        price_text.move_to(ORIGIN)
        price_text.scale(0.6)
        price_text.set_z_index(3)
        self.add(price_text)
        
        self.play(GrowFromCenter(price_text), run_time=0.5)
        self.play(price_text.animate.scale(1.0 / 0.6), run_time=2.0)
        
        orbit_phrases = [
            ("no barrier to entry", 2.2, 0.4),
            ("maximum accessibility", 2.5, 0.35),
            ("150K first-year target", 2.8, 0.3),
            ("affordable for all", 3.1, 0.25),
            ("democratizing assessment", 3.4, 0.2)
        ]
        
        orbit_mobjects = []
        for text, radius, angular_vel in orbit_phrases:
            phrase = Text(text, font="Inter", font_size=20, color="#E2E8F0")
            phrase.scale(0.5)
            phrase.move_to(ORIGIN + radius * RIGHT)
            phrase.set_z_index(3)
            orbit_mobjects.append((phrase, radius, angular_vel))
            self.add(phrase)
        
        phrase_reveal_anims = [ShowIncreasingSubsets(phrase) for phrase, _, _ in orbit_mobjects]
        self.play(LaggedStart(*phrase_reveal_anims, lag_ratio=0.15), run_time=2.5)
        
        for phrase, radius, angular_vel in orbit_mobjects:
            def make_orbit_updater(p, r, av):
                def updater(m, dt):
                    angle = av * self.renderer.time
                    new_pos = ORIGIN + r * (np.cos(angle) * RIGHT + np.sin(angle) * UP)
                    m.move_to(new_pos)
                    brightness = 0.7 + 0.3 * (0.5 + 0.5 * np.sin(angle))
                    m.set_fill_opacity(brightness)
                return updater
            phrase.add_updater(make_orbit_updater(phrase, radius, angular_vel))
        
        def price_pulse(m, dt):
            scale_val = 1.0 * (0.98 + 0.04 * (0.5 + 0.5 * np.sin(2 * np.pi * self.renderer.time * 0.5)))
            m.set_width(price_text.width * scale_val / 1.0)
        price_text.add_updater(price_pulse)
        
        self.wait(4.9)
        
        # Fade orbiting phrases to 0.4 opacity
        for phrase, _, _ in orbit_mobjects:
            phrase.clear_updaters()
        
        fade_anims = [p.animate.set_fill_opacity(0.4) for p, _, _ in orbit_mobjects]
        self.play(LaggedStart(*fade_anims, lag_ratio=0.2), run_time=2.5)

        price_text.clear_updaters()
        self.play(price_text.animate.scale(1.0), run_time=0.5)
        
        self.wait(1.42)
        
        # Section 3
        image_2 = ImageMobject("images/image_2.png")
        image_2.move_to(ORIGIN)
        image_2.set_z_index(2)
        # self.add(image_2) # GrowFromCenter adds it to scene
        
        self.play(GrowFromCenter(image_2), run_time=3.4)
        
        test_center_nodes = []
        india_nodes = []
        gcc_nodes = []
        africa_nodes = []
        sea_nodes = []
        
        for _ in range(80):
            pos = np.array([np.random.uniform(-1.5, 1.5), np.random.uniform(-1.5, 1.0), 0])
            node = Circle(radius=0.08, fill_color="#2DD4BF", fill_opacity=1, stroke_width=0)
            node.move_to(pos)
            node.set_z_index(2)
            india_nodes.append(node)
            test_center_nodes.append(node)
            self.add(node)
        
        for _ in range(35):
            pos = np.array([np.random.uniform(2.0, 4.0), np.random.uniform(-1.0, 0.5), 0])
            node = Circle(radius=0.08, fill_color="#2DD4BF", fill_opacity=1, stroke_width=0)
            node.move_to(pos)
            node.set_z_index(2)
            gcc_nodes.append(node)
            test_center_nodes.append(node)
            self.add(node)
        
        for _ in range(60):
            pos = np.array([np.random.uniform(-4.0, -1.0), np.random.uniform(-3.0, 0.0), 0])
            node = Circle(radius=0.08, fill_color="#2DD4BF", fill_opacity=1, stroke_width=0)
            node.move_to(pos)
            node.set_z_index(2)
            africa_nodes.append(node)
            test_center_nodes.append(node)
            self.add(node)
        
        for _ in range(62):
            pos = np.array([np.random.uniform(3.5, 6.0), np.random.uniform(-2.0, 0.5), 0])
            node = Circle(radius=0.08, fill_color="#2DD4BF", fill_opacity=1, stroke_width=0)
            node.move_to(pos)
            node.set_z_index(2)
            sea_nodes.append(node)
            test_center_nodes.append(node)
            self.add(node)
        
        node_reveal_anims = [ShowIncreasingSubsets(node) for node in test_center_nodes]
        self.play(LaggedStart(*node_reveal_anims, lag_ratio=0.01), run_time=3.4)
        
        connection_lines_2 = []
        for i, node_i in enumerate(test_center_nodes):
            for j, node_j in enumerate(test_center_nodes):
                if i < j and np.linalg.norm(node_i.get_center() - node_j.get_center()) < 1.2:
                    line = Line(node_i.get_center(), node_j.get_center(), color="#FF6B9A", stroke_width=0.5)
                    line.set_z_index(1)
                    connection_lines_2.append(line)
                    self.add(line)
        
        line_reveal_anims = [Create(line) for line in connection_lines_2]
        self.play(LaggedStart(*line_reveal_anims, lag_ratio=0.01), run_time=2.0)
        
        for node in test_center_nodes:
            def make_node_pulse(n, t_offset):
                def updater(m, dt):
                    scale_val = 0.08 * (0.07 + 0.02 * (0.5 + 0.5 * np.sin(2 * np.pi * (self.renderer.time + t_offset) * 0.5)))
                    m.set_width(2 * scale_val)
                return updater
            node.add_updater(make_node_pulse(node, np.random.rand()))
        
        region_labels = [
            ("India", np.array([0.5, 1.7, 0]), india_nodes),
            ("GCC", np.array([3.5, 1.3, 0]), gcc_nodes),
            ("Africa", np.array([-2.5, 0.7, 0]), africa_nodes),
            ("Southeast Asia", np.array([5.0, 0.0, 0]), sea_nodes)
        ]
        
        label_mobjects = []
        for label_text, label_pos, associated_nodes in region_labels:
            label = Text(label_text, font="Girder 117", font_size=28, color="#F8FAFC")
            label.move_to(label_pos)
            label.scale(0.7)
            label.set_z_index(3)
            label_mobjects.append((label, associated_nodes))
            self.add(label)
        
        label_reveal_anims = [ShowIncreasingSubsets(label) for label, _ in label_mobjects]
        self.play(LaggedStart(*label_reveal_anims, lag_ratio=0.5), run_time=4.0)
        
        grouped_animations = []

        for label, associated_nodes in label_mobjects:
            grouped_animations.append(
                AnimationGroup(
                    label.animate.scale(1.0 / 0.7),
                    *[node.animate.set_fill_opacity(1.2) for node in associated_nodes],
                    *[node.animate.set_fill_opacity(1.0) for node in associated_nodes],
                    lag_ratio=0.05
                )
            )

        self.play(
            LaggedStart(
                *grouped_animations,
                lag_ratio=0.15
            ),
            run_time=3
        )
        
        self.play(price_text.animate.scale(0.4), run_time=1.0)
        self.play(price_text.animate.set_fill_opacity(0.5), run_time=1.0)
        
        self.wait(3.31)
        
        # Section 4
        image_3 = ImageMobject("images/image_3.png")
        image_3.scale(0.5)
        image_3.move_to(np.array([0, 2.5, 0]))
        image_3.set_z_index(3)
        self.add(image_3)
        
        self.play(image_3.animate.scale(1.0 / 0.5), run_time=3.1)
        
        pathway_targets = [
            np.array([0.5, 1.0, 0]),
            np.array([-1.5, -0.5, 0]),
            np.array([2.0, 0.0, 0]),
            np.array([-2.5, -1.0, 0]),
            np.array([4.0, -0.5, 0])
        ]
        
        pathways = []
        for target in pathway_targets:
            pathway = Line(np.array([0, 2.5, 0]), target, color=YELLOW, stroke_width=2)
            pathway.set_z_index(2)
            pathways.append(pathway)
            self.add(pathway)
        
        pathway_anims = [Create(path) for path in pathways]
        self.play(LaggedStart(*pathway_anims, lag_ratio=0.2), run_time=2.0)
        
        for pathway in pathways:
            def make_light_updater(path):
                def updater(m, dt):
                    t = self.renderer.time % 2.5
                    progress = (t / 2.5)
                    start = path.get_start()
                    end = path.get_end()
                    light_pos = start + progress * (end - start)
                    light = Circle(radius=0.15, fill_color="#2DD4BF", fill_opacity=0.8, stroke_width=0)
                    light.move_to(light_pos)
                    light.set_z_index(2)
                return updater
            pathway.add_updater(make_light_updater(pathway))
        
        capacity_metrics = [
            ("13M assessments annually (Dexit capacity)", np.array([3.5, 3.0, 0])),
            ("3.5M on-demand capacity", np.array([3.5, 2.3, 0])),
            ("400+ global exam centers", np.array([3.5, 1.6, 0]))
        ]
        
        capacity_mobjects = []
        for metric_text, metric_pos in capacity_metrics:
            metric = Text(metric_text, font="Inter", font_size=18, color="#F8FAFC")
            metric.move_to(metric_pos)
            metric.scale(0.6)
            metric.set_z_index(3)
            capacity_mobjects.append(metric)
            self.add(metric)
        
        metric_reveal_anims = [ShowIncreasingSubsets(metric) for metric in capacity_mobjects]
        self.play(LaggedStart(*metric_reveal_anims, lag_ratio=0.4), run_time=3.0)
        
        animations_capacity = [
            metric.animate.scale(1.0 / 0.6)
            for metric in capacity_mobjects
        ]

        self.play(
            LaggedStart(
                *animations_capacity,
                lag_ratio=0.1
            ),
            run_time=2
        )

        
        operational_msgs = [
            ("On-demand, year-round testing", np.array([0, -2.5, 0]), 0.3),
            ("24/7 access", np.array([0, -3.0, 0]), 0.25),
            ("Continuous shortlisting", np.array([0, -3.5, 0]), 0.2)
        ]
        
        op_mobjects = []
        for msg_text, msg_pos, drift_speed in operational_msgs:
            msg = Text(msg_text, font="Inter", font_size=20, color="#E2E8F0")
            msg.move_to(msg_pos)
            msg.scale(0.6)
            msg.set_z_index(2)
            op_mobjects.append((msg, drift_speed))
            self.add(msg)
        
        msg_reveal_anims = [ShowIncreasingSubsets(msg) for msg, _ in op_mobjects]
        self.play(LaggedStart(*msg_reveal_anims, lag_ratio=0.3), run_time=2.0)
        
        for msg, drift_speed in op_mobjects:
            def make_drift_updater(m, speed):
                def updater(m_inner, dt):
                    m_inner.shift(np.array([0, speed * dt, 0]))
                    if m_inner.get_y() > -1.5:
                        m_inner.set_y(-4.0)
                return updater
            msg.add_updater(make_drift_updater(msg, drift_speed))
        
        grouped_animations = []

        for label, associated_nodes in label_mobjects:
            grouped_animations.append(
                AnimationGroup(
                    # Indicate label
                    Indicate(label, color="#2DD4BF"),

                    # Brighten nodes
                    *[
                        node.animate.set_fill_opacity(1.3)
                        for node in associated_nodes
                    ],

                    # Restore nodes (slightly staggered)
                    LaggedStart(
                        *[
                            node.animate.set_fill_opacity(1.0)
                            for node in associated_nodes
                        ],
                        lag_ratio=0.05
                    ),

                    lag_ratio=0.1
                )
            )

        self.play(
            LaggedStart(
                *grouped_animations,
                lag_ratio=0.2
            ),
            run_time=3
        )

        
        self.play(price_text.animate.set_fill_opacity(0.0), run_time=1.5)
        
        self.wait(3.14)
        
        # Section 5
        tagline_words = [
            ("Global", np.array([-1.2, -2.0, 0]), 0.0),
            ("Benchmark.", np.array([0.5, -2.0, 0]), 0.4),
            ("Local", np.array([-1.2, -3.0, 0]), 0.8),
            ("Access.", np.array([0.5, -3.0, 0]), 1.2)
        ]
        
        tagline_mobjects = []
        for word, word_pos, offset in tagline_words:
            word_text = Text(word, font="Girder 117", font_size=32, color="#F8FAFC")
            word_text.move_to(word_pos)
            word_text.scale(0.8)
            word_text.set_fill_opacity(0.0)
            word_text.set_z_index(3)
            tagline_mobjects.append((word_text, offset))
            self.add(word_text)
        
        word_groups = []

        for word_text, offset in tagline_mobjects:
            word_groups.append(
                AnimationGroup(
                    # Write word letter-by-letter
                    AddTextLetterByLetter(word_text),

                    # Fade to final opacity
                    word_text.animate.set_fill_opacity(0.85),

                    # Control sequencing inside the word
                    lag_ratio=1.0  # ensures fade happens after writing
                )
            )

        self.play(
            LaggedStart(
                *word_groups,
                lag_ratio=0.2
            ),
            run_time=6.5
        )

        
        pulse_freq_map = {
            0: 0.6,
            1: 0.6,
            2: 0.5,
            3: 0.5
        }
        
        for idx, (word_text, _) in enumerate(tagline_mobjects):
            freq = pulse_freq_map.get(idx, 0.5)
            def make_word_pulse(w, f):
                def updater(m, dt):
                    opacity_val = 0.85 + 0.02 * np.sin(2 * np.pi * f * self.renderer.time)
                    m.set_fill_opacity(opacity_val)
                return updater
            word_text.add_updater(make_word_pulse(word_text, freq))
        
        self.wait(5.3)
        
        # Step 1 — Clear updaters (not animated)
        for word_text, _ in tagline_mobjects:
            word_text.clear_updaters()

        # Step 2 — Build animations
        animations = [
            word_text.animate.set_fill_opacity(0.85)
            for word_text, _ in tagline_mobjects
        ]

        # Step 3 — Play once
        self.play(
            LaggedStart(
                *animations,
                lag_ratio=0.1
            ),
            run_time=1.2
        )

        
        self.wait(2.4)

if __name__ == "__main__":
    config.processes = 4  # Use 4 CPU cores
    config.max_files_cached = 200  # Helps with memory management
    config.progress_bar = "none"
    config.enable_cuda = True
    config.disable_caching = True
    #config.background_color = "#ffffff"
    config.pixel_height = 360
    config.pixel_width = 640
    config.frame_rate = 15
    #config.pixel_height = 180
    #config.pixel_width = 320
    #config.frame_rate = 10
    from pathlib import Path
    import shutil

    scene_to_render = FinalScene()
    scene_to_render.render()

    file_dir = Path(r"../manim_test_videos")
    file_dir.mkdir(exist_ok=True)
    file_name = "group_2.mp4"
    file_path = file_dir / file_name
    

    try:
        media_dir = Path("media/videos")
        latest_video = sorted(media_dir.glob("**/*.mp4"),
                                key=lambda f: f.stat().st_mtime, reverse=True)[0]
        shutil.move(str(latest_video), str(file_path))
        print(f"Video moved to {file_path}")
    except IndexError:
        print("No video file was generated by Manim.")