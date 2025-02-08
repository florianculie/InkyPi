from plugins.base_plugin.base_plugin import BasePlugin 
from datetime import datetime
from utils.image_utils import get_image
from PIL import Image, ImageOps
import logging
from plugins.french_newspaper.constants import NEWSPAPERS


logger = logging.getLogger(__name__)

#                                   YYYY/MM/DD/fr/newspapername
KIOSKO_IMAGE_URL = "https://img.kiosko.net/{}/fr/{}.750.jpg"
class FrenchNewspaper(BasePlugin):
    def generate_image(self, settings, device_config):
        newspaper_slug = settings.get('newspaperSlug')

        if not newspaper_slug:
            raise RuntimeError("Newspaper input not provided.")
        today = datetime.today()

        image_url = KIOSKO_IMAGE_URL.format(today.strftime('%Y/%m/%d'), newspaper_slug)
        image = get_image(image_url)
        if image:
            logging.info(f"Found {newspaper_slug} front cover for {today.strftime('%Y-%m-%d')}")
            # expand height if newspaper is wider than resolution
            img_width, img_height = image.size
            desired_width, desired_height = device_config.get_resolution()

            img_ratio = img_width / img_height
            desired_ratio = desired_width / desired_height

            if img_ratio < desired_ratio:
                new_height = int((img_width*desired_width) / desired_height)
                new_image = Image.new("RGB", (img_width, new_height), (255, 255, 255))
                new_image.paste(image, (0,0))
                size = (400, 800)
                padded_image = ImageOps.pad(new_image, size, color="#fff")
                image = padded_image
        else:
            raise RuntimeError("Newspaper front cover not found.")
        return image
    
    def generate_settings_template(self):
        template_params = super().generate_settings_template()
        template_params['newspapers'] = sorted(NEWSPAPERS, key=lambda n: n['name'])
        return template_params