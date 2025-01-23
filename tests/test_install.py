from scvi_colab import install


def test_install():
    install(run_outside_colab=True, version="0.14.0")
