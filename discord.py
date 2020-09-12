from dhooks import Webhook, Embed

def send_alert(webhook, stores, proxies):

    # Sends alert to Discord webhook re: monitor.
    
    hook = Webhook(webhook)
    embed = Embed(
        color=0x43b581,
        title="Monitor started!",
        timestamp="now"
    )
    stores_str = "\n".join(stores)
    
    embed.add_field(name="Stores",
                    value=stores_str,
    )
    embed.add_field(name="Proxies",
                    value=len(proxies),
    )
    hook.send(embed=embed)

def send_product(webhook, store, product_info):

    # Sends ATC links for variants as a Discord message.

    hook = Webhook(webhook) 
    embed = Embed(
        color=0x5CDBF0,
        title=product_info["title"],
        url=f"https://{store}/products/{product_info['handle']}",
        timestamp="now"
    )
    embed.set_author(name=store)
    if "image" in product_info:
        embed.set_thumbnail(product_info["image"])   
    for variant in product_info["variants"]:
        if variant["available"]:
            embed.add_field(name=f"{variant['title']} - ${variant['price']}",
                            value=f"[ATC](https://{store}/cart/{variant['id']}:1)",
                            inline=False)   
    hook.send(embed=embed)