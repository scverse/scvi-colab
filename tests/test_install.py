from scvi_colab import install


def test_install():
    install(run_outside_colab=True, version="1.1.2")
